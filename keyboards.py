from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from main import db


def start_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    key_words = KeyboardButton(text="КЛЮЧЕВЫЕ СЛОВА 🎯")
    unexcept_word = KeyboardButton(text="ИСКЛЮЧАЮЩИЕ СЛОВА🚫")
    pay = KeyboardButton(text="ОПЛАТА💰")
    help_ = KeyboardButton(text="ПОМОЩЬ 🆘")
    chats = KeyboardButton(text="ЧАТЫ🔎")
    keyboard.add(key_words, unexcept_word, chats, pay, help_)
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
        delete_keywords,
        back_to_main_menu)
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
        unexcept_delete_keywords,
        back_to_main_menu)
    return keyboard


def chats_list_():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    all_chats = KeyboardButton(text="Мои чаты")
    add_chat = KeyboardButton(
        text="Добавить новый чат")
    delete_chat = KeyboardButton(
        text="Удалить все чаты")
    back_to_main_menu = KeyboardButton(text="В главное меню")
    from_all_chats = KeyboardButton(text="Собирать из всех чатов")
    keyboard.add(all_chats,
                 add_chat,
                 delete_chat,
                 from_all_chats,
                 back_to_main_menu)
    return keyboard


def words_list(words):
    keyboard = InlineKeyboardMarkup(row_width=3)

    try:
        for word in words:
            button = InlineKeyboardButton(text=word, callback_data=word)
            keyboard.add(button)

    except Exception as ex:
        print(ex)

    return keyboard


def chats_key(words):
    keyboard = InlineKeyboardMarkup(row_width=3)

    try:
        for word in words:
            if len(word) >= 15:
                button = InlineKeyboardButton(
                    text=word, callback_data=word[:20])
                keyboard.add(button)
            else:
                button = InlineKeyboardButton(text=word, callback_data=word)
                keyboard.add(button)
            print(word)
    except Exception as ex:
        print(ex)

    return keyboard


def back():
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton(text="Назад"))


def links(message=None, chat_id=None, user=None):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if chat_id is None:
        chat = f"https://t.me/joinchat/{db.get_chat_link(chat_id)}"
        keyboard.add(InlineKeyboardButton(text="Чат", url=chat))
    else:
        chat = f"https://t.me/{chat_id}"
        keyboard.add(InlineKeyboardButton(text="Чат", url=chat))
    if message:
        keyboard.add(InlineKeyboardButton(text="Сообщение", url=message))
    if "None" not in user:
        keyboard.add(InlineKeyboardButton(
            text="Ответить", url=user))
    return keyboard
