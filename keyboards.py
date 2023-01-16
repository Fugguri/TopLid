from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from main import db


def start_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    key_words = KeyboardButton(text="Ключевые слова🎯")
    unexcept_word = KeyboardButton(text="Исключающие слова🚫")
    pay = KeyboardButton(text="Оплата💰")
    help_ = KeyboardButton(text="Помощь🆘")
    chats = KeyboardButton(text="Чаты🔎")
    info = KeyboardButton(text="Информация о TopLid_bot")
    keyboard.add(key_words, unexcept_word, chats, pay, help_, info)
    return keyboard


def info():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keys = KeyboardButton(text="Кейсы")
    instruction = KeyboardButton(text="Инструкция")
    feedback = KeyboardButton(text="Отзывы")
    keyboard.add(keys, instruction, feedback)
    back_to_main_menu = KeyboardButton(text="В главное меню")
    keyboard.add(back_to_main_menu)
    return keyboard


def keywords_list():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keywords_list = KeyboardButton(text="Список ключевых слов")
    delete_keywords = KeyboardButton(text="Удалить все ключевые слова")
    add_keyword = KeyboardButton(text="Добавить новое ключевое слово")
    back_to_main_menu = KeyboardButton(text="В главное меню")
    keyboard.add(
        add_keyword,
        keywords_list,
        delete_keywords).add(back_to_main_menu)
    return keyboard


def unexcept_keywords_list():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    unexcept_keywords_list = KeyboardButton(text="Список исключающих слов")
    unexcept_delete_keywords = KeyboardButton(
        text="Удалить все исключающие слова")
    unexcept_add_keyword = KeyboardButton(
        text="Добавить новое исключающее слово")
    back_to_main_menu = KeyboardButton(text="В главное меню")
    keyboard.add(
        unexcept_add_keyword,
        unexcept_keywords_list,
        unexcept_delete_keywords).add(back_to_main_menu)
    return keyboard


def chats_list_(telegram_id: int):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    all_chats = KeyboardButton(text="Мои чаты")
    add_chat = KeyboardButton(text="Добавить новый чат")
    back_to_main_menu = KeyboardButton(text="В главное меню")
    parse_message = KeyboardButton(text="Поиск по чатам(в разработке)")
    delete_chat = KeyboardButton(text="Удалить все чаты")
    keyboard.add(all_chats, add_chat).add(delete_chat)
    if db.get_status(telegram_id) == 1:
        keyboard.add(KeyboardButton(text="Собирать из моих чатов"))
    else:
        keyboard.add(KeyboardButton(text="Собирать из всех чатов"))
    keyboard.add(parse_message)
    keyboard.add(back_to_main_menu)
    return keyboard


def isall(telegram_id):
    print(1)


def words_list(words):
    keyboard = InlineKeyboardMarkup(row_width=3)
    try:
        for word in words:
            if len(word) >= 15:
                button = InlineKeyboardButton(
                    text=word[0], callback_data=word[1])
                keyboard.add(button)
            else:
                button = InlineKeyboardButton(
                    text=word[0], callback_data=word[1])
                keyboard.add(button)

    except Exception as ex:
        print(ex)

    return keyboard


def chats_key(words):
    keyboard = InlineKeyboardMarkup(row_width=3)

    try:
        for word in words:
            if len(word[0]) >= 15:
                button = InlineKeyboardButton(
                    text=word[0][:30], callback_data=word[1])
                keyboard.add(button)
            else:
                button = InlineKeyboardButton(
                    text=word[0], callback_data=word[1])
                keyboard.add(button)
    except Exception as ex:
        print(ex)

    return keyboard


def back():
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton(text="Назад"))


def links(message=None, chat_id=None, user=None):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if chat_id is None:
        chat = f"https://t.me/joinchat/{db.get_chat_link(chat_id)}"
        keyboard.add(InlineKeyboardButton(
            text="Чат", callback_data=chat))
    else:
        chat = f"https://t.me/{chat_id}"
        keyboard.add(InlineKeyboardButton(
            text="Чат", callback_data=chat))
    if message:
        keyboard.add(InlineKeyboardButton(text="Сообщение",
                                          callback_data=message))
    if "None" not in user:
        keyboard.add(InlineKeyboardButton(
            text="Ответить", callback_data=user))

    return keyboard


def message_collector_week_range():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        text=f'Сообщения за 1 неделю', callback_data=f'1 week'))
    keyboard.add(InlineKeyboardButton(
        text=f'Сообщения за 2 недели', callback_data=f'2 week'))
    keyboard.add(InlineKeyboardButton(
        text=f'Сообщения за 3 недели', callback_data=f'3 week'))
    keyboard.add(InlineKeyboardButton(
        text=f'Сообщения за 4 недели', callback_data=f'4 week'))
    return keyboard
