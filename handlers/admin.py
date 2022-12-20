from main import dp, dp
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import start_keyboard, keywords_list, unexcept_keywords_list, words_list, back, chats_list_, chats_key
from aiogram.dispatcher.filters import Text
from aiogram import types


class Admin(StatesGroup):
    ferify = State()
    pay = State()
    add_admin = State()


admin_markup = types.InlineKeyboardMarkup()
admin_markup.add(types.InlineKeyboardButton(
    text="Добавить пользователя", callback_data="Добавить пользователя"))
admin_markup.add(types.InlineKeyboardButton(
    text="Добавить администратора", callback_data="Добавить администратора"))
admin_markup.add(types.InlineKeyboardButton(
    text="Назад", callback_data="Назад"))

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
    await message.answer(text="Введите пароль администратора", reply_markup=None)


@ dp.message_handler(state=Admin.ferify)
async def is_correct(message: types.Message):
    if message.text == "TopLidAdmin":
        await message.answer("Выберите команду", reply_markup=admin_markup)
        await Admin.next()
    else:
        message.answer("Неверно!\nПопробуйте еще раз")
