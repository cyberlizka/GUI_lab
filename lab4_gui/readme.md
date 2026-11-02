# Lab 4 — Painter (PyQt5 + QML)

## Задача
Взять каркас приложения painter из `lab4_template` (backend на PyQt5, frontend на QML) и в классе `Interface` реализовать логику сохранения области рисования Canvas по таймеру в файл.

## Что сделано
QML не изменялся — вся новая логика сосредоточена в классе `Interface` в `main.py`.

* В `Interface` создан `QTimer`, срабатывающий каждые 5 секунд.
* По таймеру backend рекурсивно находит QML-элемент Canvas в визуальном дереве окна (`QQuickCanvasItem`).
* Изображение Canvas получается через `grabToImage()` (асинхронно, через сигнал `ready`).
* Готовый `QImage` сохраняется в PNG в папку `paintings/` с именем вида `painting_YYYYMMDD_HHMMSS.png`.

## Структура
```text
lab4_gui/
├── main.py           # backend: Interface + QTimer + сохранение
├── mainWindow.qml    # окно painter, Canvas, панель инструментов
├── Circle.qml        # компонент выбора толщины
└── Square.qml        # компонент выбора цвета

# Запуск

python main.py

# Проверка

1. Запустить `python main.py` — открывается окно painter.
2. Порисовать в белой области.
3. Подождать 5 секунд — в консоли появится `Сохранено: paintings/painting_...png`.
4. Открыть PNG — на нём только содержимое Canvas, без панели инструментов и рамок окна.
5. Дорисовать — следующий PNG содержит обновлённое состояние.

# Ключевые моменты реализации

- `QTimer` живет в `Interface` → логика «по таймеру» в backend-классе.
- Поиск Canvas — по визуальному дереву (`contentItem().childItems()`), т.к. QML не трогаем.
- `grabToImage()` асинхронный — ссылка на результат хранится в `self._last_grab`, иначе возможен GC до `ready`.
- `saveImage(QImage)` — слот с проверкой `isNull()`, сохранением через `QImage.save()`, в папку `paintings/`.
