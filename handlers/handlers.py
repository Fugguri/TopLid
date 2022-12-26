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
    telegram_id = message.from_user.id
    db.create_user(telegram_id,
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


@ dp.message_handler(Text(equals='ИСКЛЮЧАЮЩИЕ СЛОВА🚫'))
async def unexcepted_keywords_list(message: types.Message):
    await message.answer(text="В этом меню вы можете добавить, настроить или удалить исключающие слова",
                         reply_markup=unexcept_keywords_list())


@ dp.message_handler(Text(equals=['КЛЮЧЕВЫЕ СЛОВА 🎯', "Назад"]))
async def keywords(message: types.Message):
    await message.answer(text='''Бот выполняет поиск по ключевым словам в Telegram чатах и каналов. На данный момент в боте база чатов и каналов больше 35000 (Каждый раз база растет)

Здесь вы можете задать/удалить слова и фразы, по которым будет осуществляться поиск в чатах.

Для того, чтобы поиск начал работать, не забудьте оплатить подписку по кнопке ОПЛАТА💰
Так же если у вас есть своя база чатов и каналов то добавить их можно в меню “Чаты🔎”..''', reply_markup=keywords_list())


@ dp.message_handler(Text(equals='ЧАТЫ🔎'))
async def chat_list(message: types.Message):
    await message.answer(text='''Тут вы можете добавить свой список чатов и каналов, по которым будет проходить поиск лидов для вас 🎯\nВы можете выбрать чаты из нашей базы или переключиться на свои кнопной "Из базы чатов"''',
                         reply_markup=chats_list_(message.from_user.id))


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
