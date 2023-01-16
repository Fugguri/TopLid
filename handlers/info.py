from asyncio import sleep
import calendar
import datetime
from keyboards import info
from aiogram.dispatcher.filters import Text
from aiogram import types
from main import dp, db, bot, logger


@dp.message_handler(Text("Информация о TopLid_bot"))
async def information(message: types.Message):
    logger.debug(f"{message.from_user}Информация TopLid")
    await message.answer(text="Выберете интересующий вас раздел", reply_markup=info())


@dp.message_handler(Text("Кейсы"))
async def information(message: types.Message):
    logger.debug(f"{message.from_user}Кейсы")
    await message.answer(text="https://teletype.in/@son2421/4AJsTKODWKU")


@dp.message_handler(Text("Отзывы"))
async def information(message: types.Message):
    logger.debug(f"{message.from_user}Отзывы")
    await message.answer(text="https://t.me/+y-8lrkdi3VFkMDIy")


@dp.message_handler(Text("Инструкция"))
async def information(message: types.Message):
    logger.debug(f"{message.from_user}Инструкция")
    await message.answer(text="https://www.youtube.com/watch?v=cz9x6inj6zI")
