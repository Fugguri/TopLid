from asyncio import sleep
from aiogram.dispatcher.filters import Text
from aiogram import types
from mailer_bot import dp, bot, logger
from aiogram.dispatcher.filters.state import State, StatesGroup
from pathlib import Path
from telethon import TelegramClient


class Base_state(StatesGroup):
    add_base = State()
    add_account = State()
    enter_code = State()


phone_code_hash = " текст рассылки"
text = ""
client_data = []
back = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton("Назад"))
keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton(
    text="Загрузка базы", callback_data="Загрузка базы"))
keyboard.add(types.InlineKeyboardButton(
    text="Запуск рассылки", callback_data="Запуск рассылки"))
keyboard.add(types.InlineKeyboardButton(
    text="Добавить аккаунт", callback_data="Добавить аккаунт"))


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    logger.debug(f'{message.from_user}Кнопка старт')
    await message.answer(text="Добро пожаловать! Чтоты задать текст сообщения введите команду /text и текст рассылки в одном сообщении.\nПример '/text текст рассылки'", reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data == "Загрузка базы")
async def add_base(callback: types.CallbackQuery):
    await Base_state.add_base.set()
    await callback.message.answer("Отправьте файл")


@dp.message_handler(content_types=["document"], state=Base_state.add_base)
async def get_dock(message: types.Message, state: State):
    try:
        print(message.document)
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        dot_index = message.document.file_name.index(".")
        file_expancion = message.document.file_name[dot_index:]
        file_on_disk = Path(
            "files/", f"{message.from_user.id}{file_expancion}")
        await bot.download_file(file_path, destination=file_on_disk,)
        await message.answer("Успешно", reply_markup=back)
    except Exception as ex:
        print(ex)
        await message.answer("Неудача", reply_markup=back)


@dp.message_handler(Text(equals="Назад"), state=Base_state)
async def get_dock(message: types.Message, state: State):
    await state.finish()
    await message.answer(text="Главное меню", reply_markup=keyboard)


@dp.message_handler(commands=["text"])
async def add_base(message: types.Message):
    global text
    text = message.get_args()
    await message.answer(f"Текст рассылки:{text}")


@dp.callback_query_handler(lambda call: call.data == "Добавить аккаунт")
async def add_account(callback: types.CallbackQuery):
    await Base_state.add_account.set()
    await callback.message.reply("Введите данные профиля: Api_id, Api_hash, phone_number")


@dp.message_handler(state=Base_state.add_account)
async def accound_data_handler(message: types.Message):
    try:
        print(message.text)
        print(message.text.split(" "))
        api_id, api_hash, phone_number = message.text.replace(
            ",", " ").split(" ")
        print(api_id, api_hash)
        global client_data
        client_data = [phone_number, api_id, api_hash]
        client = TelegramClient(phone_number, api_id, api_hash)
        try:
            await Base_state.enter_code.set()
            global phone_code_hash
            await client.connect()
            if not await client.is_user_authorized():
                await client.send_code_request(phone_number)
                phone_code_hash = await client.send_code_request(
                    phone_number).phone_code_hash
            await message.answer("Запрос кода отправлен на сервер: Введите код из сообщения.Если код не приходит попробуйте другой профиль(Возможны ошибки).")
            with open("clients_data.txt", "a") as file:
                file.write(phone_number + " " +
                           api_id + " " + api_hash+"\n")
            await client.disconnect()
        except Exception as ex:
            await client.disconnect()
            await message.answer(f"Ошибка {ex}, проверьте данные или подождите")
    except Exception as ex:
        await client.disconnect()
        await message.answer(f"Ошибка {ex}, проверьте данные или подождите")


@dp.message_handler(state=Base_state.enter_code)
async def accound_data_handler(message: types.Message):
    await message.answer(f"Код принят, проверяю")
    global client_data
    global phone_code_hash
    code = message.text
    try:
        phone_number, api_id, api_hash = client_data[0], client_data[1], client_data[2]
        client = TelegramClient(phone_number, api_id, api_hash)
        await client.connect()
        me = await client.sign_in(phone_number, int(code), phone_code_hash=phone_code_hash)
        await message.answer(f"Успешно добавлен профиль:{me}")
        await client.disconnect()
    except Exception as ex:
        await client.disconnect()
        await message.answer(f"Ошибка {ex}, проверьте данные")
