from asyncio import sleep
import calendar
import datetime
from keyboards import start_keyboard, keywords_list, unexcept_keywords_list, words_list, back, chats_list_, chats_key
from aiogram.dispatcher.filters import Text
from aiogram import types
from main import dp, db, bot
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddWord(StatesGroup):
    word = State()


''' Ключевые слова !!!'''


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


@ dp.message_handler(Text(equals='Удалить все ключевые слова'))
async def unexcepted_keywords_list(message: types.Message):
    if db.is_pay(message.from_user.id) is False:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")
    else:
        db.delete_all(message.from_user.id, 'users_keywords')
        await message.answer(text="Вы удалили все ключевые слова.\n Не забудьте добавить новые!",
                             reply_markup=keywords_list())


@ dp.message_handler(Text(equals='Список ключевых слов'))
async def unexcepted_keywords_list(message: types.Message):
    if db.is_pay(message.from_user.id):
        keywords = db.all_words(message.from_user.id)
        await message.answer(text="Список ключевых слов!\nЧтобы удалить, нажмите на слово!",
                             reply_markup=words_list(keywords))
    else:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")


@ dp.message_handler(Text(equals='Добавить новое ключевое слово'))
async def add_word_menu(message: types.Message):
    if db.is_pay(message.from_user.id):
        await AddWord.word.set()
        await message.answer(text="Введите ключевое слово", reply_markup=back())
    else:

        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")


@ dp.message_handler(Text(equals="Назад"), state=AddWord.word)
async def add_word(message: types.Message, state: State):
    await state.finish()
    await message.answer(text='Бот выполняет поиск по ключевым словам.'
                         'Вы можете задать/удалить слова и фразы, по которым будет осуществляться поиск в чатах в пункте меню "Добавить новые слова" ниже\n\n'
                         'Для того, чтобы поиск начал работать, не забудьте добавить чаты в меню “Чаты”, в которых нужно отслеживать ключевые слова.',
                         reply_markup=keywords_list())


@ dp.callback_query_handler(lambda call: call.data in db.all_words(call['from']['id']))
async def remove_word(call: types.CallbackQuery):
    keywords = db.remove_keyword(call['from']['id'], call.data)
    await call.message.answer("Список ключевых слов!\n Чтобы удалить, нажмите на слово!",
                              reply_markup=words_list(keywords))


@ dp.callback_query_handler(lambda call: call.data in db.all_words(call['from']['id']), state=AddWord.word)
async def remove_word(call: types.CallbackQuery):
    keywords = db.remove_keyword(call['from']['id'], call.data)
    await call.message.answer("Список ключевых слов!\n Чтобы удалить, нажмите на слово!",
                              reply_markup=words_list(keywords))


@ dp.message_handler(state=AddWord.word)
async def add_word(message: types.Message):
    telegram_id = message.from_user.id,
    db.add_keyword(telegram_id, str(message.text))
    keywords = db.all_words(telegram_id)
    await message.answer(
        text="Ваши ключевые слова\nЧтобы удалить нажми на слово", reply_markup=words_list(keywords))
