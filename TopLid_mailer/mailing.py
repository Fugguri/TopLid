from asyncio import sleep
from aiogram.dispatcher.filters import Text
from aiogram import types
from mailer_bot import dp, bot, logger
from aiogram.dispatcher.filters.state import State, StatesGroup
from pathlib import Path
from telethon import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
from handlers import text
SLEEP_TIME = 30


@dp.callback_query_handler(lambda call: call.data == "Запуск рассылки")
async def add_base(callback: types.CallbackQuery):
    from handlers import text
    api_id = 27044267
    api_hash = 'a7448d0befc9804176b9c917898d923a'
    phone_number = '+79283529546'
    client = TelegramClient(phone_number, api_id, api_hash)
    await client.connect()
    receiver = await client.get_input_entity(248184623)
    await client.send_message(receiver, text)
    receiver = await client.get_input_entity(5909883622)
    await client.send_message(receiver, text)
    # with open("clients_data.txt", "r") as file:
    #     for i in file.readlines():
    #         # api_id, api_hash, phone_number = i.split(" ")
    #         api_id = 27044267
    #         api_hash = 'a7448d0befc9804176b9c917898d923a'
    #         phone_number = '+79283529546'
    #         client = TelegramClient(phone_number, api_id, api_hash)
    #         await client.connect()
    #         receiver = await client.get_input_entity(248184623)
    #         await client.send_message(receiver, text)
#     with open(f"{callback.from_user.id}.txt") as data:
#         users = data.readlines()
#         for user in users:
#             if user == "":
#                 continue
#             receiver = client.get_input_entity(user)
#             try:
#                 client.send_message(receiver, text)
#                 print("[+] Waiting {} seconds".format(SLEEP_TIME))
#                 sleep(SLEEP_TIME)
#             except PeerFloodError:
#                 print(
#                     "[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
#                 client.disconnect()
#             except Exception as e:
#                 print("[!] Error:", e)
#                 print("[!] Trying to continue...")
#                 continue
#         client.disconnect()
#         print("Done. Message sent to all users.")
# await callback.message.answer("Функция рассылки требует доработки.")


def send_sms(users, message, phone, api_id, api_hash):

    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('[+] Enter the code: '))
