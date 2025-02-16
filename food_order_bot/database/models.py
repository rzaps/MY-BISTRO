# Файл models.py нужен, чтобы структурировать работу с базой данных.  Вместо
# того, чтобы писать SQL-запросы вручную, удобнее работать через Python-классы.
# #
# Что будет в models.py?
# Классы для работы с БД (User, MenuItem, Order).
# Методы для работы с пользователями, меню и заказами.
# Логика получения данных, добавления и обновления записей.

# Объяснение кода
# 🔹 Работа с пользователями (User)
# add_user(telegram_id, name) – добавляет пользователя в БД, если его еще нет.
# get_user(telegram_id) – получает ID и имя пользователя.
# 🔹 Работа с меню (MenuItem)
# get_categories() – получает список всех категорий блюд.
# get_dishes_by_category(category) – получает блюда по выбранной категории.
# 🔹 Работа с заказами (Order)
# create_order(user_id, items, total_price) – создает новый заказ.
# get_orders(user_id) – получает все заказы конкретного пользователя.
# update_status(order_id, new_status) – обновляет статус заказа (например,
# "готов", "в пути").

import sqlite3

DB_NAME = "database.db"  # Имя файла базы данных

# === Класс пользователя ===
class User:
    @staticmethod
    def add_user(telegram_id, name):
        """Добавляет нового пользователя в БД"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (telegram_id, name) VALUES (?, ?)", (telegram_id, name))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user(telegram_id):
        """Получает пользователя по Telegram ID"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users WHERE telegram_id = ?", (telegram_id,))
        user = cursor.fetchone()
        conn.close()
        return user  # (id, name) или None

# === Класс для работы с меню ===
class MenuItem:
    @staticmethod
    def get_categories():
        """Получает список всех уникальных категорий блюд"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM menu")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories

    @staticmethod
    def get_dishes_by_category(category):
        """Получает блюда в указанной категории"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, image_url FROM menu WHERE category = ?", (category,))
        dishes = cursor.fetchall()
        conn.close()
        return dishes  # [(id, name, price, image_url), ...]

# === Класс заказов ===
class Order:
    @staticmethod
    def create_order(user_id, items, total_price):
        """Создает новый заказ"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (user_id, items, total_price, status) VALUES (?, ?, ?, 'pending')",
                       (user_id, items, total_price))
        conn.commit()
        conn.close()

    @staticmethod
    def get_orders(user_id):
        """Получает все заказы пользователя"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, items, total_price, status FROM orders WHERE user_id = ?", (user_id,))
        orders = cursor.fetchall()
        conn.close()
        return orders  # [(id, items, total_price, status), ...]

    @staticmethod
    def update_status(order_id, new_status):
        """Обновляет статус заказа"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        conn.commit()
        conn.close()

