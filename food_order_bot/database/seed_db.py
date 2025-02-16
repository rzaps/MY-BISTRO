# Запусти seed_db.py (скрипт для добавления тестовых данных)

import sqlite3

# Подключение к базе данных
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Тестовые блюда с изображениями
menu_items = [
    ("Пицца Маргарита", "Пицца", 550, "https://img.freepik.com/free-photo/top-view-pepperoni-pizza-with-mushroom-sausages-bell-pepper-olive-corn-black-wooden_141793-2158.jpg"),
    ("Паста Карбонара", "Паста", 450, "https://img.freepik.com/free-photo/spaghetti-carbonara-with-bacon-parmesan-cheese_2829-11244.jpg"),
    ("Бургер Чизбургер", "Бургеры", 300, "https://img.freepik.com/free-photo/delicious-burger-with-many-ingredients-isolated-white-background-tasty-cheeseburger-sesame-bun_90220-1192.jpg"),
    ("Суши Филадельфия", "Суши", 700, "https://img.freepik.com/free-photo/sushi-set-with-salmon-rolls_140725-2292.jpg")
]

# Добавление данных в БД
cursor.executemany("INSERT INTO menu (name, category, price, image_url) VALUES (?, ?, ?, ?)", menu_items)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Тестовые данные с изображениями добавлены!")
