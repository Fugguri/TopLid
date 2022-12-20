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

#     await add_word()

# links_ = ['3jEiz-LRF5E4MDJi', 'AY8kjWpE_U4wODc6', 'AY8kjWpE_U4wODc6', 'CyGAnUwHNsHqM7ymSEQT0A', 'DiVhlvzQPY8xMDgy', 'Doqdj-qbjfY2NmNi', 'exchange_reklama', 'adm_telegram', 'tgm_adm', 'tgm_trade', 'trade_tgm', 'dvijenie_telegram', 'piarNOpar', 'qSHHb07VCm8zNTEy', 'z12CYsIbtrkxYzZh', 'fQ0ZAAsetodkMGZi', 'Po7Kjl6GTrlhMzRi', '8b0xNR4WaH9mZTFi', 'Ld4BggAk8KszNTZh', 'iGaRzs9IDKo0Y2Qy', 'NVUl3pmRGOIwMmMx', 'o0UkYEKA44A1YzJh', '2OV6mVrJRWkyZDky', 'cDHaVzQdYrYwNDRi', '24dusMZlQgk4OTcy', '0jIVcFn-8gtmOWI6', 'M2TwyjbS2NliNmMy', '1K4pIe73QZQ4MTUy', 'YczkQTbfxys0OTBi', '75bDB9sRHzI4MzZi', 'hJbkhbBO_540Y2Fi', 'ZvyO25hfO4o1NGIy', '6IDDBiy2W7dhNWU6', '6IDDBiy2W7dhNWU6', '6IDDBiy2W7dhNWU6', 'mb2UaSwa1JAwN2My', '-UuYAyyp2HNlYTIx', 'COIvySwtDGxhMGZh',
#           'CdpOMGL1UThjZjM0', 'OyOdO7qS-1c5NDMy', 'B2BpJnHzVXkxOTIy', 'T_3fqy7FStwxNWJi', '0pecYNr9sH1hYzZi', '1KLxyVaVX1E5OTgy', 'sDWLbNAaxEg3MWQy', 'sDWLbNAaxEg3MWQy', '2UFhMaxrQVk0NjUy', 'CiWvkww3qCZlNGVi', 'DRBAnSMQu2JkYzIy', '77FJR676i3c5ZWYy', '233WUAoflDcwNjBi', 'HI8lBOMl2do4YmNi', 'HY602kycZK9kMDVi', 'GAha9KymF584MzIy', 'ajN1eVpqUMk0NWJi', 'T5ZIEqlu19M2MGEy', 'mrP6ZkIOID1hMGNi', 'Y9IVESLYHrlkMWQy', 'u7PVQHCsEqk0MzY6', 'oB_b5q2zF1YxMjFi', 'qPKvjpJA9GE3MzY6', '5GwtnIpJxdBmZmUy', 'I5C4350uvm82ZWEy', 'OglxuCHdyno1YzU6', 'ZWyis-IMAQljYmYy', 'VukUpsB40dQ3NmQy', 'LZv38lLzc842ZjVi', 'M_HYCshaXNc2ZjJi', '-X6w5YLQ3BplNDMy', 'r0EmqC3T-ytkNzVi', 'jgAganXZ-xQ1MTMy', 'RK0UhEP5iaSdyRht6r8ZRQ', 'UNmC0UT8drk91MbfNGoQrQ', 'RK0UhEP5iaSdyRht6r8ZRQ']


async def on_shutdown(_):
    print("Бот остановлен")


# async def add_word():
#     for i in links_:
#         try:
#             await bot.send_message(chat_id=5593323077, text=f'/request {i} {248184623}')
#             print("Succes")
#             await sleep(3)
#         except:
#             print("EXC")
#             pass
#     print("Done")


if __name__ == "__main__":
    import subprocess
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
