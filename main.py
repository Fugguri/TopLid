from aiogram import Bot, Dispatcher, executor
from config import TOKEN_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DB_connectors.MySql_connect import Database
import traceback
from asyncio import sleep
# from flask import Flask, request, Response

# app = Flask(__name__)


# @app.route("/", methods=["POST", "GET"])
# def index():
#     if request.headers.get('content-type')=='applycation/json':
#         update =


storage = MemoryStorage()
bot = Bot(TOKEN_API, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage,)
db = Database("TopLid")


async def on_startup(_):
    print("Бот запущен")
    db.cbdt()


async def on_shutdown(_):
    print("Бот остановлен")


# if __name__ == "__main__":
#     app.run()
if __name__ == "__main__":
    from handlers import dp
    # while True:
    #     try:
    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
    # except Exception as e:
    #     traceback.print_exc()
    #     print(e)
    #     sleep(1)
