import sqlite3
from datetime import datetime, timedelta
import random

DB_NAME = "db.sqlite"

# Подключение к БД
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# 1. Таблица users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER,
        registration_date DATE
    )
''')

# 2. Таблица departments
cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT
    )
''')

# 3. Таблица employees
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department_id INTEGER,
        salary REAL,
        hire_date DATE,
        FOREIGN KEY (department_id) REFERENCES departments (id)
    )
''')

# 4. Таблица products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL,
        category TEXT
    )
''')

# 5. Таблица orders
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        order_date DATE,
        total REAL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
''')

# Покупатели
names = [
    "Анна Петрова", "Борис Сидоров", "Виктория Соколова", "Геннадий Орлов",
    "Дарья Козлова", "Евгений Медведев", "Жанна Киселева", "Захар Егоров",
    "Инна Павлова", "Кирилл Степанов"
]
emails = [f"client_{i}_flower@mail.ru" for i in range(1, 11)]

# Отделы магазина
departments = [
    ("Оранжерея", "Теплица №1"),
    ("Флористика", "Торговый зал"),
    ("Логистика", "Склад"),
    ("Бухгалтерия", "Офис 2"),
    ("Маркетинг", "Офис 1")
]

# Товары (Цветы и инвентарь)
products = [
    ("Роза красная", 150.0, "Цветы"),
    ("Тюльпан желтый", 80.0, "Цветы"),
    ("Орхидея Фаленопсис", 450.0, "Цветы"),
    ("Горшок керамический", 350.0, "Инвентарь"),
    ("Грунт универсальный", 200.0, "Инвентарь"),
    ("Удобрение жидкое", 120.0, "Химия"),
    ("Лейка садовая", 400.0, "Инвентарь"),
    ("Букет 'Весенний'", 1500.0, "Букеты"),
    ("Суккулент Микс", 250.0, "Цветы"),
    ("Открытка поздравительная", 50.0, "Сопутствующие")
]

# Вставка данных в users
for i in range(10):
    name = names[i]
    email = emails[i]
    age = random.randint(18, 70)
    reg_date = (datetime.now() - timedelta(days=random.randint(1, 365*2))).strftime('%Y-%m-%d')
    cursor.execute("INSERT OR IGNORE INTO users (name, email, age, registration_date) VALUES (?, ?, ?, ?)",
                   (name, email, age, reg_date))

# Вставка данных в departments
for dept in departments:
    cursor.execute("INSERT OR IGNORE INTO departments (name, location) VALUES (?, ?)", dept)

# Вставка данных в products
for prod in products:
    cursor.execute("INSERT OR IGNORE INTO products (name, price, category) VALUES (?, ?, ?)", prod)

# Вставка данных в employees (Флористы, грузчики и т.д.)
for i in range(15):
    name = f"Специалист {i+1}"
    dept_id = random.randint(1, len(departments))
    salary = round(random.uniform(25000, 90000), 2)
    hire_date = (datetime.now() - timedelta(days=random.randint(1, 365*4))).strftime('%Y-%m-%d')
    cursor.execute("INSERT OR IGNORE INTO employees (name, department_id, salary, hire_date) VALUES (?, ?, ?, ?)",
                   (name, dept_id, salary, hire_date))

# Вставка данных в orders (Заказы на цветы)
for i in range(30):
    user_id = random.randint(1, 10)
    product_id = random.randint(1, len(products))
    quantity = random.randint(1, 3)
    order_date = (datetime.now() - timedelta(days=random.randint(0, 180))).strftime('%Y-%m-%d')
    total = round(products[product_id - 1][1] * quantity, 2)
    cursor.execute("INSERT OR IGNORE INTO orders (user_id, product_id, quantity, order_date, total) VALUES (?, ?, ?, ?, ?)",
                   (user_id, product_id, quantity, order_date, total))

conn.commit()
conn.close()

print(f"База данных '{DB_NAME}' успешно создана и заполнена.")
