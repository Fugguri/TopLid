from aiogram import Bot, Dispatcher, executor
from config import TOKEN_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DB_connectors.MySql_connect import Database
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

storage = MemoryStorage()
bot = Bot(TOKEN_API, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
db = Database("TopLid")
py_handler = logging.FileHandler(f"logs/{__name__}.log", mode='w')
logger.addHandler(py_handler)


async def on_startup(_):
    print("Бот запущен")
    logger.debug("Запущен бот!")
    db.cbdt()


async def on_shutdown(_):
    print("Бот остановлен")


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
