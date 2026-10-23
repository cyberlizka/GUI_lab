import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl


class CurrencyConverterWidget(QWidget):
    _API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

    def __init__(self, usd_signals, eur_signals, rub_signals, common_signals):
        super().__init__()

        self.usd_signals = usd_signals
        self.eur_signals = eur_signals
        self.rub_signals = rub_signals
        self.common_signals = common_signals

        self._rates = {}
        self._net = QNetworkAccessManager()

        self._net.finished.connect(self._on_network_reply)

        self._build_ui()
        self._wire_signals()
        self._fetch_rates()

    def _build_ui(self):
        self.setWindowTitle('Конвертер валют')
        self.setMinimumWidth(380)

        root = QVBoxLayout(self)

        self._usd_edit = QLineEdit()
        self._eur_edit = QLineEdit()
        self._rub_edit = QLineEdit()

        for caption, field in (
            ('Доллары (USD):', self._usd_edit),
            ('Евро (EUR):', self._eur_edit),
            ('Рубли (RUB):', self._rub_edit),
        ):
            root.addWidget(QLabel(caption))
            root.addWidget(field)

        self._reset_btn = QPushButton('Очистить все поля')
        root.addWidget(self._reset_btn)

    def _wire_signals(self):
        # Внешние сигналы
        self.usd_signals.usd_changed.connect(self._recalc_from_usd)
        self.eur_signals.eur_changed.connect(self._recalc_from_eur)
        self.rub_signals.rub_changed.connect(self._recalc_from_rub)

        # Общие сигналы
        self.common_signals.clear_all.connect(self._reset_fields)
        self.common_signals.rates_updated.connect(self._store_rates)

        self._usd_edit.textEdited.connect(self._emit_usd)
        self._eur_edit.textEdited.connect(self._emit_eur)
        self._rub_edit.textEdited.connect(self._emit_rub)

        self._reset_btn.clicked.connect(self._request_reset)

    def _fetch_rates(self):
        self._net.get(QNetworkRequest(QUrl(self._API_URL)))

    def _on_network_reply(self, reply: QNetworkReply):
        if reply.error() != QNetworkReply.NoError:
            print('Ошибка сети:', reply.errorString())
            reply.deleteLater()
            return

        try:
            payload = json.loads(bytes(reply.readAll().data()))
            table = self._make_conversion_table(payload.get('rates') or {})

            if not table:
                print('В ответе API нет нужных валют')
            else:
                self.common_signals.rates_updated.emit(table)

        except (ValueError, TypeError) as exc:
            print('Ошибка разбора JSON:', exc)

        reply.deleteLater()

    @classmethod
    def _make_conversion_table(cls, base_rates):
        to_eur = base_rates.get('EUR')
        to_rub = base_rates.get('RUB')
        if not to_eur or not to_rub:
            return {}

        def from_usd(rate_to_usd, rate_from_usd):
            return rate_from_usd / rate_to_usd

        return {
            ('USD', 'EUR'): to_eur,
            ('USD', 'RUB'): to_rub,
            ('EUR', 'USD'): from_usd(to_eur, 1.0),
            ('EUR', 'RUB'): from_usd(to_eur, to_rub),
            ('RUB', 'USD'): from_usd(to_rub, 1.0),
            ('RUB', 'EUR'): from_usd(to_rub, to_eur),
        }

    def _store_rates(self, table):
        self._rates = table

    @staticmethod
    def _parse_amount(text):
        try:
            return float(text.replace(',', '.'))
        except ValueError:
            return None

    def _emit_usd(self, text):
        value = self._parse_amount(text)
        if value is not None: self.usd_signals.usd_changed.emit(value)

    def _emit_eur(self, text):
        value = self._parse_amount(text)
        if value is not None: self.eur_signals.eur_changed.emit(value)

    def _emit_rub(self, text):
        value = self._parse_amount(text)
        if value is not None: self.rub_signals.rub_changed.emit(value)

    def _recalc_from_usd(self, amount): self._apply('USD', amount)
    def _recalc_from_eur(self, amount): self._apply('EUR', amount)
    def _recalc_from_rub(self, amount): self._apply('RUB', amount)

    def _apply(self, source, amount):
        if not self._rates: return

        targets = {'USD': self._usd_edit, 'EUR': self._eur_edit, 'RUB': self._rub_edit}
        for code, field in targets.items():
            if code == source: continue
            field.setText(f'{amount * self._rates[(source, code)]:.2f}')

    def _reset_fields(self):
        self._usd_edit.clear()
        self._eur_edit.clear()
        self._rub_edit.clear()

    def _request_reset(self):
        self.common_signals.clear_all.emit()
