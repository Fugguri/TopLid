from main import dp, db
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import start_keyboard, keywords_list, unexcept_keywords_list, words_list, back, chats_list_, chats_key
from aiogram.dispatcher.filters import Text
from aiogram import types
import datetime
import calendar


class Admin(StatesGroup):
    ferify = State()
    pay = State()
    add_admin = State()


admin_markup = types.InlineKeyboardMarkup()
admin_markup.add(types.InlineKeyboardButton(
    text="Добавить пользователя(оплачен доступ)", callback_data="Добавить пользователя"))
admin_markup.add(types.InlineKeyboardButton(
    text="Добавить администратора", callback_data="Добавить администратора"))
admin_markup.add(types.InlineKeyboardButton(
    text="Назад", callback_data="Назад"))

back_key = types.InlineKeyboardMarkup()
back_key.add(types.InlineKeyboardButton(
    text="Назад", callback_data="В меню"))
# add_user = types.InlineKeyboardMarkup(
#     [types.InlineKeyboardButton(text="Назад", callback_data="Назад")])
# add_admin = types.InlineKeyboardMarkup([
# add_admin.add(types.InlineKeyboardButton(text="", callback_data=""),
#     types.InlineKeyboardButton(text="", callback_data=""),
#     types.InlineKeyboardButton(
#         text="Назад", callback_data="Назад")
# ])


@ dp.message_handler(commands=["admin"])
async def admin_cab(message: types.Message):
    await Admin.ferify.set()
    if message.from_user.username in ["fugguri", 'son2421'] or message.from_user.username in db.is_admin(message.from_user.username):
        await message.answer("Выберите команду", reply_markup=admin_markup)
    else:
        await message.answer(text="Введите пароль администратора")


@ dp.message_handler(state=Admin.ferify)
async def is_correct(message: types.Message):
    if message.text == "TopLidAdmin":
        await message.answer("Выберите команду", reply_markup=admin_markup)
    else:
        await message.answer("Неверно!\nПопробуйте еще раз")


@dp.callback_query_handler(lambda call: call.data == "Добавить пользователя", state=Admin.ferify)
async def back(callback: types.CallbackQuery):
    await callback.message.answer("Введите ник(username) пользователя", reply_markup=back_key)
    await Admin.pay.set()


@dp.message_handler(state=Admin.pay)
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


@dp.callback_query_handler(lambda call: call.data == "Добавить администратора", state=Admin.ferify)
async def back(callback: types.CallbackQuery):
    await callback.message.answer(
        "Введите ник(username) пользователя", reply_markup=back_key)
    await Admin.add_admin.set()


@dp.message_handler(state=Admin.add_admin)
async def back(message: types.CallbackQuery):
    if message.from_user.username in ["fugguri", 'son2421'] or message.from_user.username in db.is_admin(message.from_user.username):
        admin = str(message.text)
        db.add_admin(admin)
        await message.answer("Успешно")
    else:
        print("Вы не администратор")


@dp.message_handler(commands=["annul"])
async def set_time(message: types.Message):
    if db.is_admin(message.from_user.username) or message.from_user.username in ['son2421', "fugguri"]:
        x = datetime.datetime.now()
        user = str(message.get_args())
        subscription_end = add_months(x, -1)
        try:
            db.pay(user, str(subscription_end))
            await message.answer("Успешно!")
        except:
            await message.answer(
                "Ошибка!\nПроверьте данные или обратитесь к администратору!")
    else:
        await message.answer("Вы не администратор")


@dp.callback_query_handler(lambda call: call.data == "Назад", state=Admin)
async def admin_add(callback: types.CallbackQuery, state: State):
    await callback.message.answer("Вы в главном меню", reply_markup=start_keyboard())
    await state.finish()


@dp.callback_query_handler(lambda call: call.data == "В меню", state=Admin)
async def admin_add(callback: types.CallbackQuery, state: State):
    await state.finish()
    await callback.message.answer("Выберите команду", reply_markup=admin_markup)
    await Admin.ferify.set()


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
