# Что делает этот файл?
#
# Загружает меню из базы данных.
# Разбивает его на категории.
# Показывает пользователю список доступных блюд.

# Команда /menu
# 🔹 Показывает пользователю список категорий из базы.
# 🔹 Создает кнопки с названиями категорий.
# 🔹 Если меню пустое, отправляет сообщение.
#
# Обработчик выбора категории
# 🔹 Пользователь выбирает категорию.
# 🔹 Бот загружает список блюд из базы.
# 🔹 Отправляет фото блюда + цену.
#
# Зависимости
# Для работы menu.py нужны:
#
# models.py – получает категории и блюда.
# bot.py – главный объект бота.
# telebot – для отправки сообщений и фото


# Что изменилось?
# Добавлены кнопки "➕ Добавить в корзину"
#
# Используем InlineKeyboardMarkup() и InlineKeyboardButton().
# callback_data=f"add_{dish_id}" — передаем ID блюда в callback.
# Когда пользователь нажимает кнопку, вызывается обработчик в order.py.
# Теперь show_dishes() отправляет не просто список блюд, а
#
# Картинку блюда.
# Название и цену.
# Кнопку для добавления в корзину.
#
# 1️⃣ show_dishes() добавлена в menu.py
# 2️⃣ Когда пользователь выбирает категорию, бот отправляет ему список блюд
# 3️⃣ Для каждого блюда отображается:
#
# Фото блюда
# Название + цена
# Кнопки "Добавить в корзину" и "Удалить"




import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import MenuItem
from bot import bot


# === Команда /menu ===
@bot.message_handler(commands=['menu'])
def show_menu(message):
    """Отображает пользователю список категорий блюд"""
    categories = MenuItem.get_categories()

    if categories:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=True)
        for category in categories:
            keyboard.add(telebot.types.KeyboardButton(category))
        bot.send_message(message.chat.id, "Выберите категорию:",
                         reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Меню пока пустое!")


# === Обработчик выбора категории ===
@bot.message_handler(
    func=lambda message: message.text in MenuItem.get_categories())
def show_dishes(message):
    """Отображает список блюд в выбранной категории с кнопками 'Добавить в корзину'"""
    category = message.text
    dishes = MenuItem.get_dishes_by_category(category)

    if dishes:
        for dish_id, name, price, image_url in dishes:
            # Создаем inline-кнопки "Добавить" и "Удалить"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("➕ Добавить",
                                            callback_data=f"add_{dish_id}"))
            markup.add(InlineKeyboardButton("❌ Удалить",
                                            callback_data=f"remove_{name}"))

            # Отправляем изображение блюда, его название и цену + кнопки
            bot.send_photo(message.chat.id, image_url,
                           caption=f"{name} - {price}₽", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "В этой категории пока нет блюд.")
