import sys
import os
from datetime import datetime

from PyQt5.QtCore import QObject, pyqtSlot, QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickItem, QQuickWindow


class Interface(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.save_dir = "paintings"
        os.makedirs(self.save_dir, exist_ok=True)

        self._window = None
        self._canvas = None
        self._last_grab = None
        self._dumped = False

        self._timer = QTimer(self)
        self._timer.setInterval(5000)
        self._timer.timeout.connect(self._on_timeout)
        self._timer.start()

    def set_root(self, root):
        self._window = root


    def _find_canvas(self):
        if self._window is None:
            return None
        if isinstance(self._window, QQuickWindow):
            root_item = self._window.contentItem()
        else:
            root_item = self._window
        if root_item is None:
            return None
        return self._search_canvas(root_item)

    def _search_canvas(self, item):
        if item is None:
            return None
        try:
            cn = item.metaObject().className()
        except Exception:
            cn = ""
        if cn == "QQuickCanvasItem" or "Canvas" in cn:
            return item
        for child in item.childItems():
            found = self._search_canvas(child)
            if found is not None:
                return found
        return None

    def _dump_tree(self, item, depth=0):
        if item is None:
            return
        print("  " * depth + item.metaObject().className())
        for child in item.childItems():
            self._dump_tree(child, depth + 1)

    # таймер

    def _on_timeout(self):
        if self._canvas is None:
            self._canvas = self._find_canvas()

        if self._canvas is None:
            if not self._dumped:
                print("Canvas не найден. Дерево элементов окна:")
                if self._window is not None:
                    root_item = (self._window.contentItem()
                                 if isinstance(self._window, QQuickWindow)
                                 else self._window)
                    self._dump_tree(root_item)
                self._dumped = True
            return

        self._last_grab = self._canvas.grabToImage()
        if self._last_grab is None:
            print("grabToImage вернул None")
            return
        self._last_grab.ready.connect(self._on_grab_ready)

    def _on_grab_ready(self):
        img = self._last_grab.image() if self._last_grab else None
        self._last_grab = None
        self.saveImage(img)

    # ---- слот сохранения (как в вашем образце) ----

    @pyqtSlot(QImage)
    def saveImage(self, image: QImage):
        if image and not image.isNull():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.save_dir}/painting_{timestamp}.png"
            if image.save(filename):
                print(f"Сохранено: {filename}")
            else:
                print(f"Ошибка сохранения: {filename}")
        else:
            print("Получено пустое изображение")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    interface = Interface()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("_backend", interface)
    engine.load("mainWindow.qml")

    if not engine.rootObjects():
        print("Ошибка: Не удалось загрузить QML файл!")
        sys.exit(-1)

    interface.set_root(engine.rootObjects()[0])

    sys.exit(app.exec())
