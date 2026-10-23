import sys

from PyQt5.QtWidgets import QApplication

from usd_signals import UsdSignals
from eur_signals import EurSignals
from rub_signals import RubSignals
from common_signals import CommonSignals
from currency_converter import CurrencyConverterWidget


def build_signal_bus():
    """
    Создаёт все объекты-сигналы и возвращает их одним словарём.
    """
    return {
        'usd': UsdSignals(),
        'eur': EurSignals(),
        'rub': RubSignals(),
        'common': CommonSignals(),
    }


def main():
    app = QApplication(sys.argv)

    bus = build_signal_bus()

    window = CurrencyConverterWidget(
        bus['usd'],
        bus['eur'],
        bus['rub'],
        bus['common'],
    )
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
