from asyncio import sleep
import calendar
import datetime
from keyboards import start_keyboard, keywords_list, unexcept_keywords_list, words_list, back, chats_list_, chats_key
from aiogram.dispatcher.filters import Text
from aiogram import types
from main import dp, db, bot
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddUnex_Word(StatesGroup):
    word = State()


'''Исключающие слова !!!'''


@ dp.message_handler(Text(equals='Удалить все исключающие слова'))
async def unexcepted_keywords_list(message: types.Message):
    await message.answer(text="Вы удалили все исключающие слова.\n Не забудьте добавить новые!",
                         reply_markup=unexcept_keywords_list())
    db.delete_all(message.from_user.id, 'users_unex_words')


@ dp.message_handler(Text(equals='Список исключающих слов'))
async def unexcepted_keywords_list(message: types.Message):
    if db.is_pay(message.from_user.id):
        keywords = db.all_unex_words(message.from_user.id)
        await message.answer(text="Список илючающих слов!\n Чтобы удалить, нажмите на слово!",
                             reply_markup=words_list(keywords))
    else:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")


@ dp.message_handler(Text(equals='Добавить новое исключающее слово'))
async def add_word_menu(message: types.Message):
    if db.is_pay(message.from_user.id):
        await AddUnex_Word.word.set()
        await message.answer(text="Введите исключающее слово", reply_markup=back())
    else:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")


@ dp.message_handler(Text(equals="Назад"), state=AddUnex_Word.word)
async def add_word(message: types.Message, state: State):
    await state.finish()
    await message.answer(text='Бот выполняет поиск по ключевым словам.'
                         'Вы можете задать/удалить слова и фразы, по которым будет осуществляться поиск в чатах в пункте меню "Добавить новые слова" ниже\n\n'
                         'Для того, чтобы поиск начал работать, не забудьте добавить чаты в меню “Чаты”, в которых нужно отслеживать ключевые слова.',
                         reply_markup=unexcept_keywords_list())


@ dp.message_handler(state=AddUnex_Word.word)
async def add_word(message: types.Message):
    db.add_unex_word(message.from_user.id, str(message.text))
    keywords = db.all_unex_words(message.from_user.id)
    await message.answer(
        text="Ваши исключающие слова\nЧтобы удалить нажми на слово", reply_markup=words_list(keywords))


@ dp.callback_query_handler(lambda call: call.data in db.all_unex_words(call['from']['id']), state=AddUnex_Word.word)
async def remove_word(call: types.CallbackQuery):
    keywords = db.remove_unex_word(call['from']['id'], call.data)
    await call.message.answer("Список ключевых слов!\n Чтобы удалить, нажмите на слово!",
                              reply_markup=words_list(keywords))
