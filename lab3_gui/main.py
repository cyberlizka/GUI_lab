import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QTabWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTableWidget,
    QTableWidgetItem, QMessageBox, QFileDialog
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt


class DatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQLite Database Viewer")
        self.resize(850, 600)

        self.database_conn = None
        self.active_table_name = None

        self.build_ui()
        self.init_default_tab()

    def build_ui(self):
        # Главное меню
        main_menu = self.menuBar()
        db_menu = main_menu.addMenu("Menu")

        act_open = QAction("Set connection", self)
        act_open.triggered.connect(self.connect_db)
        db_menu.addAction(act_open)

        act_close = QAction("Close connection", self)
        act_close.triggered.connect(self.disconnect_db)
        db_menu.addAction(act_close)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Вкладки
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        self.data_tables = self.create_tab_pages()

        # Панель управления
        control_panel = QHBoxLayout()

        self.btn_col = QPushButton("bt1 'SELECT Column'")
        self.btn_col.clicked.connect(self.query_bt1)
        control_panel.addWidget(self.btn_col)

        self.combo_cols = QComboBox()
        self.combo_cols.addItem("Выберите колонку...")
        self.combo_cols.currentIndexChanged.connect(self.on_combo_changed)
        control_panel.addWidget(self.combo_cols)

        self.btn_q2 = QPushButton("bt2 'Query2'")
        self.btn_q2.clicked.connect(self.query_bt2)
        control_panel.addWidget(self.btn_q2)

        self.btn_q3 = QPushButton("bt3 'Query3'")
        self.btn_q3.clicked.connect(self.query_bt3)
        control_panel.addWidget(self.btn_q3)

        layout.addLayout(control_panel)

    def create_tab_pages(self):
        """Создает 5 вкладок с пустыми таблицами"""
        tables = []
        for i in range(1, 6):
            page = QWidget()
            page_layout = QVBoxLayout(page)
            grid = QTableWidget()
            grid.setColumnCount(0)
            grid.setRowCount(0)
            page_layout.addWidget(grid)
            tables.append(grid)
            self.tab_widget.addTab(page, f"Tab{i}")
        return tables

    def init_default_tab(self):
        """Заполнение первой вкладки по умолчанию"""
        if self.database_conn and self.database_conn.isOpen():
            self.render_results("SELECT * FROM sqlite_master", self.data_tables[0])

    def connect_db(self):
        """Открытие файла базы данных"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть базу данных", "", "SQLite Files (*.db *.sqlite)"
        )
        if not file_path:
            return

        if self.database_conn and self.database_conn.isOpen():
            self.database_conn.close()

        self.database_conn = QSqlDatabase.addDatabase("QSQLITE")
        self.database_conn.setDatabaseName(file_path)

        if not self.database_conn.open():
            QMessageBox.critical(self, "Ошибка", f"Сбой подключения: {self.database_conn.lastError().text()}")
            self.database_conn = None
            return

        QMessageBox.information(self, "Успех", "Подключение установлено!")
        self.init_default_tab()
        self.load_columns_to_combo()

    def disconnect_db(self):
        """Закрытие соединения и очистка"""
        if self.database_conn and self.database_conn.isOpen():
            self.database_conn.close()
            self.database_conn = None

            QMessageBox.information(self, "Информация", "Соединение закрыто.")

            for grid in self.data_tables:
                grid.setRowCount(0)
                grid.setColumnCount(0)

            self.combo_cols.clear()
            self.combo_cols.addItem("Выберите колонку...")

    def load_columns_to_combo(self):
        """Получение списка колонок для QComboBox"""
        if not self.database_conn or not self.database_conn.isOpen():
            return

        query = QSqlQuery()
        query.exec_("SELECT name FROM sqlite_master WHERE type='table'")

        tables = []
        while query.next():
            tables.append(query.value(0))

        if tables:
            self.active_table_name = tables[0]
            col_query = QSqlQuery()
            col_query.exec_(f"PRAGMA table_info({self.active_table_name})")

            columns = []
            while col_query.next():
                col_name = col_query.value(1)
                if col_name:
                    columns.append(col_name)

            self.combo_cols.clear()
            self.combo_cols.addItem("Выберите колонку...")
            self.combo_cols.addItems(columns)

    def query_bt1(self):
        """bt1: Список таблиц -> Tab2"""
        if not self.database_conn or not self.database_conn.isOpen():
            QMessageBox.warning(self, "Предупреждение", "Сначала установите соединение!")
            return
        self.render_results("SELECT name FROM sqlite_master", self.data_tables[1])

    def on_combo_changed(self):
        """Событие выбора колонки -> Tab3"""
        selected = self.combo_cols.currentText()

        if selected == "Выберите колонку..." or not self.database_conn or not self.database_conn.isOpen():
            return

        if not self.active_table_name:
            QMessageBox.warning(self, "Предупреждение", "Таблица не выбрана.")
            return

        sql = f"SELECT {selected} FROM {self.active_table_name} LIMIT 10"
        self.render_results(sql, self.data_tables[2])

    def query_bt2(self):
        """bt2: Запрос -> Tab4"""
        if not self.database_conn or not self.database_conn.isOpen():
            QMessageBox.warning(self, "Предупреждение", "Сначала установите соединение!")
            return
        self.render_results("SELECT * FROM sqlite_master WHERE type='table' LIMIT 5", self.data_tables[3])

    def query_bt3(self):
        """bt3: Запрос -> Tab5"""
        if not self.database_conn or not self.database_conn.isOpen():
            QMessageBox.warning(self, "Предупреждение", "Сначала установите соединение!")
            return
        self.render_results("SELECT sql FROM sqlite_master WHERE type='table' LIMIT 3", self.data_tables[4])

    def render_results(self, sql_string, target_grid):
        """Заполняет QTableWidget результатами запроса"""
        query = QSqlQuery()

        # Здесь мы выполняем запрос ровно один раз
        if not query.exec_(sql_string):
            error = query.lastError().text()
            QMessageBox.critical(self, "Ошибка запроса", f"Не удалось выполнить:\n{error}")
            return

        record = query.record()
        cols_count = record.count()

        if cols_count == 0:
            QMessageBox.warning(self, "Внимание", "Запрос не вернул колонок.")
            target_grid.setColumnCount(0)
            target_grid.setRowCount(0)
            return

        # Формируем заголовки
        headers = []
        for i in range(cols_count):
            field = record.fieldName(i)
            if not field:
                field = f"Column_{i + 1}"
            headers.append(field)

        target_grid.setColumnCount(cols_count)
        target_grid.setHorizontalHeaderLabels(headers)
        target_grid.setRowCount(0)

        # Заполняем данными
        row = 0
        while query.next():
            target_grid.insertRow(row)
            for col in range(cols_count):
                val = query.value(col)
                text_val = "NULL" if val is None else str(val)
                target_grid.setItem(row, col, QTableWidgetItem(text_val))
            row += 1

        # Если данных нет
        if row == 0:
            target_grid.setRowCount(1)
            empty_item = QTableWidgetItem("Нет данных")
            empty_item.setTextAlignment(Qt.AlignCenter)
            target_grid.setItem(0, 0, empty_item)
            for col in range(1, cols_count):
                target_grid.setItem(0, col, QTableWidgetItem(""))

        target_grid.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec_())
