from main import dp, db
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import start_keyboard, keywords_list, unexcept_keywords_list, words_list, back, chats_list_, chats_key
from aiogram.dispatcher.filters import Text
from aiogram import types
from datetime import date
import datetime
import calendar


class Admin(StatesGroup):
    ferify = State()
    menu = State()
    pay = State()
    add_admin = State()
    annul = State()
    add_click = State()


admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_markup.add(types.KeyboardButton(
    text="Добавить пользователя(оплачен доступ)"))
admin_markup.add(types.KeyboardButton(
    text="Добавить администратора")).add(types.KeyboardButton(
        text="Добавить попытки"))
admin_markup.add(types.KeyboardButton(
    text="Аннулировать подписку"))
admin_markup.add(types.KeyboardButton(
    text="Отчет"))
admin_markup.add(types.KeyboardButton(
    text="Назад"))

back_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_key.add(types.KeyboardButton(
    text="В меню"))


@ dp.message_handler(commands=["admin"])
async def admin_cab(message: types.Message):
    if message.from_user.username in ["fugguri", 'son2421'] or message.from_user.username in db.is_admin(message.from_user.username):
        await message.answer("Выберите команду", reply_markup=admin_markup)
        await Admin.menu.set()
    else:
        await Admin.ferify.set()
        await message.answer(text="Введите пароль администратора")


@ dp.message_handler(Text(equals="Назад"), state=Admin)
async def admin_add(message: types.Message, state: State):
    await message.answer("Вы в главном меню", reply_markup=start_keyboard())
    await state.finish()


@ dp.message_handler(Text(equals="Аннулировать подписку"), state=Admin.menu)
async def back(message: types.Message, state: State):
    await message.answer(
        "Введите ник(username) пользователя", reply_markup=back_key)
    await Admin.annul.set()


@ dp.message_handler(Text(equals="Отчет"), state=Admin.menu)
async def back(message: types.Message):
    await message.answer(
        "Собираю данные")
    users = db.get_users()
    with open("report.txt", "w") as report:
        report.write(
            "№, telegram_id, full_name, username, pay_end, click_left \n")
        count = 1
        for user in users:
            if str(user[4]) >= str(date.today()):
                data = f"{count}, {user[1]}, {user[2]}, {user[3]}, {user[4]}, {user[6]} \n"
                report.write(data)
                count += 1
    with open("report.txt", "rb") as report:
        await message.answer_document(document=report)


@ dp.message_handler(Text(equals="Добавить попытки"), state=Admin.menu)
async def back(message: types.Message, state: State):
    await message.answer(
        "Введите ник(username) пользователя и количество попыток", reply_markup=back_key)
    await Admin.add_click.set()


@ dp.message_handler(Text(equals="Добавить администратора"), state=Admin.menu)
async def back(message: types.Message, state: State):
    await message.answer(
        "Введите ник(username) пользователя", reply_markup=back_key)
    await Admin.add_admin.set()


@ dp.message_handler(Text(equals="В меню"), state=Admin)
async def admin_add(message: types.Message, state: State):
    await state.finish()
    await message.answer("Выберите команду", reply_markup=admin_markup)
    await Admin.menu.set()


@ dp.message_handler(Text(equals="Добавить пользователя(оплачен доступ)"), state=Admin.menu)
async def back(message: types.Message, state: State):
    await message.answer("Введите ник(username) пользователя", reply_markup=back_key)
    await Admin.pay.set()


@ dp.message_handler(state=Admin.ferify)
async def is_correct(message: types.Message):
    if message.text == "TopLidAdmin":
        await message.answer("Выберите команду", reply_markup=admin_markup)
        await Admin.menu.set()
    else:
        await message.answer("Неверно!\nПопробуйте еще раз")


@ dp.message_handler(state=Admin.pay)
async def back(message: types.CallbackQuery):
    if message.from_user.username in ["fugguri", 'son2421'] or message.from_user.username in db.is_admin(message.from_user.username):
        x = datetime.datetime.now()
        user = str(message.text)
        subscription_end = add_months(x, 1)
        try:
            db.pay(user, str(subscription_end))
            await message.answer("Успешно!")
        except:
            await message.answer(
                "Ошибка!\nПроверьте данные или обратитесь к администратору!")
    else:
        await message.answer("Вы не администратор")


@ dp.message_handler(state=Admin.add_admin)
async def back(message: types.CallbackQuery):
    if message.from_user.username in ["fugguri", 'son2421'] or message.from_user.username in db.is_admin(message.from_user.username):
        admin = str(message.text)
        db.add_admin(admin)
        await message.answer("Успешно")
    else:
        await message.answer("Вы не администратор")


@ dp.message_handler(state=Admin.add_click)
async def add_click(message: types.CallbackQuery):
    if message.from_user.username in ["fugguri", 'son2421'] or message.from_user.username in db.is_admin(message.from_user.username):
        command = str(message.text).split(" ")
        amount = command[1]
        user = command[0]
        try:
            db.click_add(amount, user)
            await message.answer("Успешно")
        except:
            await message.answer("Ошибка")
    else:
        await message.answer("Вы не администратор")


@ dp.message_handler(state=Admin.annul)
async def set_time(message: types.Message):
    if db.is_admin(message.from_user.username) or message.from_user.username in ['son2421', "fugguri"]:
        x = datetime.datetime.now()
        subscription_end = add_months(x, -1)
        try:
            db.pay(message.text, str(subscription_end))
            await message.answer("Успешно!")
        except:
            await message.answer(
                "Ошибка!\nПроверьте данные или обратитесь к администратору!")
    else:
        await message.answer("Вы не администратор")


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


@ dp.message_handler(commands=["TG"])
async def TGreqs(message: types.Message):
    url = str(message.get_args())
    from other.tgstat import get_page
    text = "\n".join(get_page(1, url))
    print(text)
    await message.answer(text=text)
