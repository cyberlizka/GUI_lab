Lab 4 — Painter (PyQt5 + QML)
Лабораторная работа №4 по дисциплине «Основы проектирования графического интерфейса компьютерных систем».

Задача
Взять каркас приложения painter из lab4_template (backend на PyQt5, frontend на QML) и в классе Interface реализовать логику сохранения области рисования Canvas по таймеру в файл.

Что сделано
QML не изменялся — вся новая логика сосредоточена в классе Interface в main.py.

В Interface создан QTimer, срабатывающий каждые 5 секунд.

По таймеру backend рекурсивно находит QML-элемент Canvas в визуальном дереве окна (QQuickCanvasItem).

Изображение Canvas получается через grabToImage() (асинхронно, через сигнал ready).

Готовый QImage сохраняется в PNG в папку paintings/ с именем вида painting_YYYYMMDD_HHMMSS.png.

Структура
text
lab4_gui/
├── main.py           # backend: Interface + QTimer + сохранение
├── mainWindow.qml    # окно painter, Canvas, панель инструментов
├── Circle.qml        # компонент выбора толщины
└── Square.qml        # компонент выбора цвета
Запуск
bash
pip install PyQt5
python main.py
Откроется окно Paint!. Рисуйте мышью — каждые 5 секунд текущее состояние Canvas будет сохраняться в paintings/.

Проверка
Запустить python main.py — открывается окно painter.

Порисовать в белой области.

Подождать 5 секунд — в консоли появится Сохранено: paintings/painting_...png.

Открыть PNG — на нём только содержимое Canvas, без панели инструментов и рамок окна.

Дорисовать — следующий PNG содержит обновлённое состояние.
