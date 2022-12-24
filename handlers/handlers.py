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


class AddUnex_Word(StatesGroup):
    word = State()


class AddChat(StatesGroup):
    chat = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    start_date = datetime.date.today()  # год, месяц, число
    result_date = start_date - datetime.timedelta(days=1)
    await message.answer(text="""TopLid_bot помогает искать лидов и заказы  в телеграм по ключевым словам 🔎
Бот производит поиск по всем чатам и каналам  в Telegram 🔎

Чтобы получать лидов:
📌Добавьте ключевые слова через пункт меню «Ключевые слова»
📌Если у вас есть своя база чатов то добавьте ее в  пункте меню «Чаты». В боте уже больше 10 000 чатов и 15 000 каналов, каждый раз база пополняется.
📌Получайте лидов в бот и отвечайте мгновенно через ссылку «Ответить» в конце сообщения (у пользователя должна быть открыта личка)

Подробности узнать о боте через команду /help 🆘""",
                         reply_markup=start_keyboard())
    db.create_user(message.from_user.id,
                   message.from_user.full_name, message.from_user.username, str(result_date))


@dp.message_handler(lambda message: 'Ссылка на чат' in message.text)
async def asd(message: types.Message):
    await bot.send_message(chat_id=248184623, text=message.text)
    # await bot.send_message(chat_id=1358110465, text=str(message.text))


@dp.message_handler(Text(equals='ОПЛАТА💰'))
async def pay(message: types.Message):
    await message.answer(text="Для получения доступа \nНапишите @son2421")


@dp.message_handler(Text(equals='ПОМОЩЬ 🆘'))
async def help(message: types.Message):
    await message.answer(text="По всем вопросам @son2421")


@dp.message_handler(Text(equals='В главное меню'))
async def main_menu(message: types.Message):
    await message.answer(text="Вы вернулись в главное меню", reply_markup=start_keyboard())

"""Команды"""


@dp.message_handler(commands=["help"])
async def set_time(message: types.Message):
    message.answer('''Как работает сервис:

Специально обученный бот сидит в каналах и группах для общения: бизнеса, поиска заказчиков и других специализированных чатах.

Он читает каждое сообщение и по определенным фильтрам и алгоритмам определяет, подходит ли для ВАС сообщение.

Как пользоваться ботом?

Чтобы начать получать лиды, вам нужно задать Ключевые слова (или фразы), по которым бот будет искать для вас сообщение.
Также вы можете задать слова, при обнаружении которых, бот проигнорирует ненужное вам сообщение.

Обычно такими словами являются нецензурные слова или фразы, а также слова и фразы ваших конкурентов''')


@dp.message_handler(commands=["delete"])
async def set_time(message: types.Message):
    word = str(message.get_args())
    db.remove_keyword_from_table(word)


@dp.message_handler(commands=["pay"])
async def set_time(message: types.Message):
    if db.is_admin(message.from_user.username):
        x = datetime.datetime.now()
        user = str(message.get_args())
        subscription_end = add_months(x, 1)
        try:
            db.pay(user, str(subscription_end))
            await message.answer("Успешно!")
        except:
            await message.answer(
                "Ошибка!\nПроверьте данные или обратитесь к администратору!")
    else:
        await message.answer("Вы не администратор")


''' Ключевые слова !!!'''


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


@ dp.message_handler(Text(equals=['КЛЮЧЕВЫЕ СЛОВА 🎯', "Назад"]))
async def keywords(message: types.Message):
    await message.answer(text='''Бот выполняет поиск по ключевым словам в Telegram чатах и каналов. На данный момент в боте база чатов и каналов больше 35000 (Каждый раз база растет)

Здесь вы можете задать/удалить слова и фразы, по которым будет осуществляться поиск в чатах.

Для того, чтобы поиск начал работать, не забудьте оплатить подписку по кнопке ОПЛАТА💰
Так же если у вас есть своя база чатов и каналов то добавить их можно в меню “Чаты🔎”..''', reply_markup=keywords_list())


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


'''Исключающие слова !!!'''


@ dp.message_handler(Text(equals='ИСКЛЮЧАЮЩИЕ СЛОВА🚫'))
async def unexcepted_keywords_list(message: types.Message):
    await message.answer(text="В этом меню вы можете добавить, настроить или удалить исключающие слова",
                         reply_markup=unexcept_keywords_list())


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


'''Чаты !!!'''


@ dp.message_handler(Text(equals='ЧАТЫ🔎'))
async def chat_list(message: types.Message):
    await message.answer(text='''Тут вы можете добавить свой список чатов и каналов, по которым будет проходить поиск лидов для вас 🎯\nВы можете выбрать чаты из нашей базы или переключиться на свои кнопной "Из базы чатов"''',
                         reply_markup=chats_list_(message.from_user.id))


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


"""Кнопка HELP !!!"""


@ dp.message_handler(commands=["help"])
async def main_menu(message: types.Message):
    await message.answer(
        text="""Как работает сервис:

Специально обученный бот сидит в группах для общения, бизнеса, поиска заказчиков и других специализированных чатах.

Он читает каждое сообщение и по определенным фильтрам и алгоритмам определяет, подходит ли для ВАС сообщение.

Как пользоваться ботом?

Чтобы начать получать лиды, вам нужно задать Ключевые слова (или фразы), по которым бот будет искать для вас сообщение.
Также вы можете задать слова, при обнаружении которых, бот проигнорирует ненужное вам сообщение.

Чтобы начать получать лиды, вам нужно задать Ключевые слова (или фразы), по которым бот будет искать для вас сообщение.
Также вы можете задать слова, при обнаружении которых, бот проигнорирует ненужное вам сообщение.

Обычно такими словами являются нецензурные слова или фразы, а также слова и фразы ваших конкурентов""",
        reply_markup=start_keyboard())

"""Админка """


@dp.message_handler(commands=['adm'])
async def login(message: types.Message):
    pass
