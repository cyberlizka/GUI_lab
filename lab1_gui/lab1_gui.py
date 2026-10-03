import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QFileDialog,
                             QMessageBox)
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt


class BackgroundWidget(QWidget):
    """Виджет-подложка, отвечающий за отрисовку полупрозрачного фона."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_image = None
        self.setAttribute(Qt.WA_TranslucentBackground)

    def set_background(self, pixmap):
        """Устанавливает новое изображение для фона и перерисовывает виджет."""
        self.background_image = pixmap
        self.update()

    def paintEvent(self, event):
        """Кастомная отрисовка фона."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.background_image and not self.background_image.isNull():
            # Масштабируем изображение, сохраняя пропорции и заполняя всю область
            scaled_pixmap = self.background_image.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            # Сдвигаем изображение для центрирования, если оно обрезается
            x_offset = (self.width() - scaled_pixmap.width()) // 2
            y_offset = (self.height() - scaled_pixmap.height()) // 2

            # Задаем полупрозрачность (70%)
            painter.setOpacity(0.7)
            painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
        else:
            # Цвет фона по умолчанию, если изображение не загружено
            painter.fillRect(self.rect(), QColor(240, 240, 240))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение с полупрозрачным фоном")
        self.resize(700, 500)

        # Создаем и устанавливаем центральный виджет
        self.bg_widget = BackgroundWidget(self)
        self.setCentralWidget(self.bg_widget)

        # Основной вертикальный слой
        main_layout = QVBoxLayout(self.bg_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Надпись по центру
        self.label = QLabel("Надпись")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: white;
            background: transparent;
        """)
        main_layout.addWidget(self.label, stretch=1)

        # Горизонтальный слой для кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)  # Расстояние между кнопками
        main_layout.addLayout(buttons_layout)

        # Кнопка 1: Смена текста
        self.btn_change_text = QPushButton("Кнопка1")
        self.btn_change_text.setMinimumHeight(35)
        self.btn_change_text.clicked.connect(self.toggle_label_text)
        buttons_layout.addWidget(self.btn_change_text)

        # Кнопка 2: Загрузка изображения
        self.btn_load_image = QPushButton("Кнопка2")
        self.btn_load_image.setMinimumHeight(35)
        self.btn_load_image.clicked.connect(self.load_background_image)
        buttons_layout.addWidget(self.btn_load_image)

    def toggle_label_text(self):
        """Переключает текст надписи."""
        if self.label.text() == "Надпись":
            self.label.setText("Текст изменён!")
        else:
            self.label.setText("Надпись")

    def load_background_image(self):
        """Загружает PNG-изображение и адаптирует размер окна."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите PNG файл",
            "",
            "Изображения (*.png *.jpg *.jpeg);;Все файлы (*.*)"
        )

        if not file_path:
            return

        try:
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                raise ValueError("Не удалось распознать формат изображения.")

            # Передаем изображение в виджет фона
            self.bg_widget.set_background(pixmap)

            # Получаем доступные размеры экрана
            screen = QApplication.primaryScreen().availableGeometry()
            screen_width = screen.width()
            screen_height = screen.height()

            img_width = pixmap.width()
            img_height = pixmap.height()

            # Если картинка больше экрана - разворачиваем на весь экран
            if img_width > screen_width or img_height > screen_height:
                self.showMaximized()
            else:
                # Если меньше - окно принимает размеры картинки
                self.resize(img_width, img_height)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", f"Произошла ошибка:\n{str(e)}")


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    # Используем стиль Fusion для более современного вида
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
