from asyncio import sleep
from datetime import date, timedelta
from keyboards import words_list, back, chats_list_, chats_key, message_collector_week_range
from aiogram.dispatcher.filters import Text
from aiogram import types
from main import dp, db, bot, logger
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils.collect_message_from_chat_client import get_message_history_by_keywords
from join_chat import connect_and_url_clean


class CollectMessage(StatesGroup):
    end_date = State()
    messages = State()
    collect_message_keywords = State()
    collect_message_unex_words = State()


collect_user_keywords_by_id = {}
collect_user_unex_words_by_id = {}

end_date_message = {}


async def word_by_id(keywords):
    kb = types.InlineKeyboardMarkup()
    for i in keywords:
        kb.add(types.InlineKeyboardButton(
            text=i, callback_data=keywords.index(i)))
    kb.add(types.InlineKeyboardButton(
        text="В меню сбора сообщений", callback_data="Назад"))
    return kb


@ dp.message_handler(Text(equals="Назад"), state=CollectMessage)
async def add_word(message: types.Message, state: State):
    await state.finish()
    await message.answer(text='Бот выполняет поиск по ключевым словам.\n'
                         'Вы можете задать / удалить слова и фразы, по которым будет осуществляться поиск в чатах в пункте меню\n"Добавить новые слова" ниже\n\n'
                         'Для того, чтобы поиск начал работать, не забудьте добавить чаты в меню “Чаты”, в которых нужно отслеживать ключевые слова.',
                         reply_markup=chats_list_(message.from_user.id))
    logger.debug(f"{message.from_user} Назад из добавление чатов")


@ dp.callback_query_handler(lambda call: call.data == "Назад", state=CollectMessage)
async def add_word(callback: types.CallbackQuery, state: State):
    await CollectMessage.end_date.set()
    logger.debug(f"{callback.message.from_user} Сбор сообщений в чатах")
    text = '''Введите период за которые будут собраны данные.
\nИли введите дату вручную. Формат YYYY-MM-DD (2020-12-20)
\nБот ищет по ключевым словам, которые вы задали в настройках. Вы можете задать ключевые и исключающие слова для поиска единоразово, нажмите на нужный раздел меню.
'''
    await callback.message.answer(text=text, reply_markup=message_collector_week_range())
    await callback.message.answer('Чтобы вернуться в меню нажмите кнопку "Назад"', reply_markup=back())


@ dp.message_handler(Text(equals="Поиск по чатам"))
async def add_word(message: types.Message, state: State):
    await CollectMessage.end_date.set()
    logger.debug(f"{message.from_user} Сбор сообщений в чатах")
    text = '''Введите период за которые будут собраны данные.
\nИли введите дату вручную. Формат YYYY-MM-DD (2020-12-20)
\nБот ищет по ключевым словам, которые вы задали в настройках. Вы можете задать ключевые и исключающие слова для поиска единоразово, нажмите на нужный раздел меню.
'''
    collect_user_keywords_by_id[message.from_user.id] = []
    collect_user_unex_words_by_id[message.from_user.id] = []

    try:
        await message.answer(text=text, reply_markup=message_collector_week_range())
        await message.answer('Чтобы вернуться в меню нажмите кнопку "Назад"', reply_markup=back())
    except:
        await message.answer(text=text, reply_markup=message_collector_week_range())
        await message.answer('Чтобы вернуться в меню нажмите кнопку "Назад"', reply_markup=back())


@ dp.callback_query_handler(lambda call: call.data == "Добавить ключевые слова", state=CollectMessage.end_date)
async def keywords(callback: types.CallbackQuery):
    await CollectMessage.collect_message_keywords.set()
    kb = await word_by_id(collect_user_keywords_by_id[callback.from_user.id])
    await callback.message.answer("Введите ключевые слова или нажмите на слово чтобы удалить", reply_markup=kb)


@ dp.message_handler(state=CollectMessage.collect_message_keywords)
async def update_keywords(message: types.Message):
    keywords = message.text.split(",")
    for i in keywords:
        collect_user_keywords_by_id[message.from_user.id].append(i)
    kb = await word_by_id(collect_user_keywords_by_id[message.from_user.id])
    await message.answer("Ключевые слова", reply_markup=kb)


@ dp.callback_query_handler(state=CollectMessage.collect_message_keywords)
async def keywords(callback: types.CallbackQuery):
    collect_user_keywords_by_id[callback.from_user.id].pop(int(callback.data))
    kb = await word_by_id(collect_user_keywords_by_id[callback.from_user.id])
    await callback.message.answer("Ключевые слова", reply_markup=kb)


@ dp.callback_query_handler(lambda call: call.data == "Добавить исключающие слова", state=CollectMessage.end_date)
async def keywords(callback: types.CallbackQuery):
    await CollectMessage.collect_message_unex_words.set()
    kb = await word_by_id(collect_user_keywords_by_id[callback.from_user.id])
    await callback.message.answer("Введите исключающие слова или нажмите на слово чтобы удалить", reply_markup=kb)


@ dp.message_handler(state=CollectMessage.collect_message_unex_words)
async def update_unex_words(message: types.Message):
    keywords = message.text.split(",")
    for i in keywords:
        collect_user_unex_words_by_id[message.from_user.id].append(i)
    kb = await word_by_id(collect_user_unex_words_by_id[message.from_user.id])
    await message.answer("Исключающие слова", reply_markup=kb)


@ dp.callback_query_handler(state=CollectMessage.collect_message_unex_words)
async def keywords(callback: types.CallbackQuery):
    collect_user_unex_words_by_id[callback.from_user.id].pop(
        int(callback.data))
    kb = await word_by_id(collect_user_unex_words_by_id[callback.from_user.id])
    await callback.message.answer("Ключевые слова", reply_markup=kb)


@ dp.callback_query_handler(lambda call: 'week' in call.data, state=CollectMessage.end_date)
async def remove_chat(callback: types.CallbackQuery):
    await CollectMessage.messages.set()
    keywords = db.all_user_chats(callback.from_user.id)
    global end_date_message
    end_date_message[callback.from_user.id] = int(callback.data.replace(
        " week", "")) * 7
    end_date_message[callback.from_user.id] = str(date.today()-timedelta(days=float(
        end_date_message[callback.from_user.id])))
    await callback.message.answer(text='Выберите чат из которого хотите выбрать данные', reply_markup=chats_key(keywords))
    logger.debug(
        f"{callback.from_user} Период времени в сборе сообщений из чатов {end_date_message[callback.from_user.id]}")


@ dp.message_handler(lambda message: message.text, state=CollectMessage.end_date)
async def add_word(message: types.Message, state: State):
    await CollectMessage.messages.set()
    keywords = db.all_user_chats(message.from_user.id)
    global end_date_message
    end_date_message[message.from_user.id] = message.text
    await message.answer(text='Выберите чат из которого хотите выбрать данные', reply_markup=chats_key(keywords))
    logger.debug(
        f"{message.from_user} Период времени в сборе сообщений из чатов {end_date_message[message.from_user.id]}")


@ dp.callback_query_handler(lambda call: call.data in list(map(lambda x: str(x[1]), db.all_user_chats(call['from']['id']))), state=CollectMessage.messages)
async def remove_chat(callback: types.CallbackQuery):
    await callback.message.answer(text='После сбора и обработки данных вам будет выслан файл с данными сообщений', reply_markup=back())
    chat_id = callback.data
    user_id = callback.from_user.id
    try:
        keywords = collect_user_keywords_by_id[callback.from_user.id]
    except:
        keywords = None
    try:
        unex_words = collect_user_unex_words_by_id[callback.from_user.id]
    except:
        unex_words = None
    await get_message_history_by_keywords(chat_id, user_id, db, end_date_message[user_id], keywords, unex_words)
    try:
        with open(f"chats/{chat_id}.txt", "rb") as w:
            await callback.message.answer_document(document=w)
            logger.debug(
                f"{callback.from_user} Отправлен файл в сборе сообщений")
    except:
        await callback.message.answer(text='Нет сообщений, удовлетворяющих запросу в данном временном промежутке ', reply_markup=back())
        logger.debug(
            f"{callback.from_user} Нет сообщений в сборе из чатов")
