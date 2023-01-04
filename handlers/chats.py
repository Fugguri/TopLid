from asyncio import sleep
import calendar
from datetime import date, timedelta
from keyboards import words_list, back, chats_list_, chats_key, message_collector_week_range
from aiogram.dispatcher.filters import Text
from aiogram import types
from main import dp, db, bot
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddChat(StatesGroup):
    chat = State()
    end_date = State()
    messages = State()


end_date_message = {}
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
        db.set_status(message.from_user.id, 1)
        await message.answer(text="Вы переключились на нашу базу чатов",
                             reply_markup=chats_list_(message.from_user.id))
    else:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")


@ dp.message_handler(Text(equals="Собирать из моих чатов"))
async def all_chat_acces(message: types.Message):
    if db.is_pay(message.from_user.id):
        db.set_status(message.from_user.id, 0)
        await message.answer(text="Вы переключились собственный список чатов",
                             reply_markup=chats_list_(message.from_user.id))
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


@ dp.message_handler(Text(equals="Назад"), state=AddChat)
async def add_word(message: types.Message, state: State):
    await state.finish()
    await message.answer(text='Бот выполняет поиск по ключевым словам.\n'
                         'Вы можете задать / удалить слова и фразы, по которым будет осуществляться поиск в чатах в пункте меню\n"Добавить новые слова" ниже\n\n'
                         'Для того, чтобы поиск начал работать, не забудьте добавить чаты в меню “Чаты”, в которых нужно отслеживать ключевые слова.',
                         reply_markup=chats_list_(message.from_user.id))


@ dp.message_handler(Text(equals="Поиск по чатам(в разработке)"))
async def add_word(message: types.Message, state: State):
    await AddChat.end_date.set()
    await message.answer(text='Введите период за которые будут собраны данные.\nИли введите дату вручную. Формат YYYY-MM-DD (2020-12-20)', reply_markup=message_collector_week_range())


@ dp.callback_query_handler(lambda call: 'week' in call.data, state=AddChat.end_date)
async def remove_chat(callback: types.CallbackQuery):
    await AddChat.messages.set()
    keywords = db.all_user_chats(callback.from_user.id)
    global end_date_message
    end_date_message[callback.from_user.id] = int(callback.data.replace(
        " week", "")) * 7
    end_date_message[callback.from_user.id] = str(date.today()-timedelta(days=float(
        end_date_message[callback.from_user.id])))
    print(end_date_message[callback.from_user.id])

    await callback.message.answer(text='Выберите чат из которого хотите выбрать данные', reply_markup=chats_key(keywords))


@ dp.message_handler(lambda message: message.text, state=AddChat.end_date)
async def add_word(message: types.Message, state: State):
    await AddChat.messages.set()
    keywords = db.all_user_chats(message.from_user.id)
    global end_date_message
    end_date_message[message.from_user.id] = message.text
    await message.answer(text='Выберите чат из которого хотите выбрать данные', reply_markup=chats_key(keywords))


@ dp.callback_query_handler(lambda call: call.data in list(map(lambda x: x[:20], db.all_user_chats(call['from']['id']))), state=AddChat.messages)
async def remove_chat(callback: types.CallbackQuery):
    text = (callback["message"]["reply_markup"]["inline_keyboard"])
    text = [i[0]['text'] for i in text if callback.data in i[0]['text']][0]
    await callback.message.answer(text='После сбора и обработки данных вам будет выслан файл с данными сообщений', reply_markup=back())
    chat_id = db.get_chat_id(text)
    user_id = callback.from_user.id
    await get_message_history_by_keywords(chat_id, user_id)

    try:
        with open(f"chats/{chat_id}.txt", "rb") as w:
            await callback.message.answer_document(document=w)
    except:
        await callback.message.answer(text='Видимо нет сообщений, удовлетворяющих запросу в данном временном промежутке ', reply_markup=back())


async def get_message_history_by_keywords(chat_id, user_id):
    from HearBot2 import clients
    for client in clients:
        print("try")
        async with client:
            # try:
            await mes(chat_id, client, user_id)
            break
            # except:
            #     print('except')
    return


async def mes(chat_id, client, user_id):
    getmessage = client.iter_messages(chat_id)
    keywords = db.all_words(user_id)
    unex_words = db.all_unex_words(user_id)
    print("try")
    with open(f"chats/{chat_id}.txt", "w") as w:
        async for message in getmessage:
            print(str(message.date)[:-15].strip(),
                  end_date_message[user_id].strip(), str(message.date)[:-15].strip() == end_date_message[user_id].strip())
            if message.message != None:
                key = any(
                    list(map(lambda x: x in message.message, keywords)))
                unex = any(
                    list(map(lambda x: x in message.message, unex_words)))
                if key and not unex:
                    mes = "\n"+str(message.date)[:-15] + \
                        message.message + \
                        "\n -------------------------------- \n"
                    w.write(mes)
            elif str(message.date)[:-15].strip() <= end_date_message[user_id].strip():
                print("fdsfsdfsdfsdfsdfsdf\n\n\n\n\n")
                return
            else:
                continue
        return


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
    await sleep(1.5)
    chats = db.all_user_chats(message.from_user.id)
    await message.answer(
        text="Ваши чаты. Добавленный чат отобразится через время, после того как бот вступит в чат.\nЧтобы удалить нажмите на название чата", reply_markup=chats_key(chats))
