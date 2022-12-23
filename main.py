from aiogram import Bot, Dispatcher, executor
from config import TOKEN_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DB_connectors.MySql_connect import Database
from asyncio import sleep
storage = MemoryStorage()
bot = Bot(TOKEN_API, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage,)
db = Database("TopLid")


async def on_startup(_):
    print("Бот запущен")
    db.cbdt()


async def on_shutdown(_):
    print("Бот остановлен")


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
