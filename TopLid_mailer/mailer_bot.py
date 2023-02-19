from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
storage = MemoryStorage()
bot = Bot("5876350183:AAFMZZMvszFV06f2ZkG6qP5LyY1fpbUNrf4", parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
py_handler = logging.FileHandler(f"logs/{__name__}.log", mode='w')
logger.addHandler(py_handler)


async def on_startup(_):
    print("Бот запущен")


async def on_shutdown(_):
    print("Бот остановлен")


if __name__ == "__main__":
    from handlers import dp
    from mailing import dp
    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
