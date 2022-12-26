from asyncio import sleep
import calendar
import datetime
from keyboards import start_keyboard, keywords_list, unexcept_keywords_list, words_list, back, chats_list_, chats_key
from aiogram.dispatcher.filters import Text
from aiogram import types
from main import dp, db, bot
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddChat(StatesGroup):
    chat = State()


'''Чаты !!!'''


@ dp.message_handler(Text(equals='Удалить все чаты'))
async def unexcepted_keywords_list(message: types.Message):
    if db.is_pay(message.from_user.id) is False:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")
    else:
        db.delete_all(message.from_user.id, 'users_chats')
        await message.answer(text="Вы удалили все чаты.\n Не забудьте добавить новые!",
                             reply_markup=chats_list_(message.from_user.id))


@ dp.message_handler(Text(equals="Собирать из всех чатов"))
async def all_chat_acces(message: types.Message):
    if db.is_pay(message.from_user.id):
        await message.answer(text="Вы переключились на нашу базу чатов",
                             reply_markup=chats_list_(message.from_user.id))
        db.set_status(message.from_user.id, 1)
    else:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")


@ dp.message_handler(Text(equals="Собирать из моих чатов"))
async def all_chat_acces(message: types.Message):
    if db.is_pay(message.from_user.id):
        await message.answer(text="Вы переключились собственный список чатов",
                             reply_markup=chats_list_(message.from_user.id))
        db.set_status(message.from_user.id, 0)
    else:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")


@ dp.message_handler(Text(equals='Мои чаты'))
async def chatse_list(message: types.Message):
    keywords = db.all_user_chats(message.from_user.id)
    text = "Список ваших чатов!\nЧтобы удалить, нажмите на чат!"
    try:
        await message.answer(text=str(text),
                             reply_markup=chats_key(keywords))
    except:
        text += '\nУ вас пока нет чатов. Вы можете их добавить нажав на кнопку "Добавить группы"'
        await message.answer(text=str(text))


@ dp.message_handler(Text(equals='Добавить новый чат'))
async def add_word_menu(message: types.Message):
    if db.is_pay(message.from_user.id):
        await AddChat.chat.set()
        await message.answer(text="Введите ссылку на чат", reply_markup=back())
    else:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")


@ dp.callback_query_handler(lambda call: call.data in list(map(lambda x: x[:20], db.all_user_chats(call['from']['id']))))
async def remove_chat(call: types.CallbackQuery):
    text = (call["message"]["reply_markup"]["inline_keyboard"])
    text = [i[0]['text'] for i in text if call.data in i[0]['text']]
    db.remove_chat(call['from']['id'], text[0])
    keywords = db.all_user_chats(call['from']['id'])
    await call.message.answer("Список ваших чатов!\nЧтобы удалить, нажмите на название чата!",
                              reply_markup=chats_key(keywords))


@ dp.message_handler(Text(equals="Назад"), state=AddChat.chat)
async def add_word(message: types.Message, state: State):
    await state.finish()
    await message.answer(text='Бот выполняет поиск по ключевым словам.\n'
                         'Вы можете задать / удалить слова и фразы, по которым будет осуществляться поиск в чатах в пункте меню\n"Добавить новые слова" ниже\n\n'
                         'Для того, чтобы поиск начал работать, не забудьте добавить чаты в меню “Чаты”, в которых нужно отслеживать ключевые слова.',
                         reply_markup=chats_list_(message.from_user.id))


@ dp.callback_query_handler(lambda call: call.data in list(map(lambda x: x[:20], db.all_user_chats(call['from']['id']))), state=AddChat.chat)
async def remove_chat(call: types.CallbackQuery):
    text = (call["message"]["reply_markup"]["inline_keyboard"])
    text = [i[0]['text'] for i in text if call.data in i[0]['text']]
    db.remove_chat(call['from']['id'], text[0])
    keywords = db.all_user_chats(call['from']['id'])

    await call.message.answer("Список ваших чатов!\nЧтобы удалить, нажмите на название чата!",
                              reply_markup=chats_key(keywords))


@ dp.callback_query_handler(lambda call: call.text in db.all_user_chats(call['from']['id']), state=AddChat.chat)
async def remove_chat(call: types.CallbackQuery):
    keywords = db.remove_chat(call['from']['id'], call.text)
    await call.message.answer("Список ключевых слов!\nЧтобы удалить, нажмите на слово!",
                              reply_markup=words_list(keywords))


@ dp.message_handler(state=AddChat.chat)
async def add_word(message: types.Message):
    await bot.send_message(chat_id=5593323077, text=f'/request {str(message.text)} {message.from_user.id}')
    await sleep(1)
    chats = db.all_user_chats(message.from_user.id)
    await message.answer(
        text="Ваши чаты. Добавленный чат отобразится через время, после того как бот вступит в чат.\nЧтобы удалить нажмите на название чата", reply_markup=chats_key(chats))
