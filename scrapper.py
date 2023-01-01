from asyncio import sleep, run
from telethon import TelegramClient, events
from telethon.tl.types import User, Channel, Chat, PeerChannel, PeerChat
from DB_connectors.MySql_connect import Database
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, ExportChatInviteRequest
from main import bot
from keyboards import links
from config import *
from telethon.errors.rpcerrorlist import InviteHashExpiredError, InviteRequestSentError, FloodWaitError, UserAlreadyParticipantError, ChannelsTooMuchError
import logging
# from pymysql.err import


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


db = Database('TopLid')
client = TelegramClient(phone3, api_id3, api_hash3)


async def main():
    dialogs = await client.get_drafts()
    for chat in dialogs:
        print(chat)
        with open(f"chats/{chat.entity.id}.txt", "w") as w:
            # w.write(chat.entity.id)
            # client.get_messages(chat.entity.id, limit=10000)
            getmessage = client.iter_messages(chat.entity.id)
            async for message in getmessage:
                if message.message != None:
                    # print(str(message.date)[:-15])
                    mes = message.message + "\n"
                    print(mes)
                    w.write(mes)
        print(message.message)

# @client.on(events.NewMessage)
# async def message(event):
#     # async for dialog in client.iter_dialogs():
#     #     # if dialog.is_channel:
#     #     print(f'{dialog.id}:{dialog.title}')
#     chat = await client.get_entity(event.chat_id)
#     username = await event.get_sender()
#     if chat is not User and chat.id != 5751517728:
#         try:
#             a = await client.get_entity(event.message.from_id.user_id)
#             a = a.bot
#         except:
#             a = False
#         # print(event.message.to_dict()['message'])
#         keywords = db.all_words_()
#         unex_words = db.all_unex_words_()
#         message_id = event.message.id
#         message_link = ""
#         final_words = []
#         final_unex_words = []
#         text = f"""{event.message.to_dict()['message']}"""
#         message_link = f't.me/c/{str(event.chat_id)[4:]}/{message_id}'
#         try:
#             username = username.username
#         except:
#             if username is not None:
#                 username = username.user_id
#             else:
#                 username = None
#         for word in keywords:
#             if word.lower() in event.message.to_dict()['message'].lower():
#                 final_words.append(word)
#         for word in unex_words:
#             if word.lower() in event.message.to_dict()['message'].lower():
#                 final_unex_words.append(word)
#         if final_words != [] and a == False:
#             if final_unex_words == []:
#                 final_unex_words == ['bcbcv', 'bvbcv']

#             users = db.mailing_users(final_words, final_unex_words)
#             for tele_id in users:
#                 if int(str(event.chat_id)[4:]) in db.all_chats(tele_id) and db.is_pay(tele_id) and db.get_status(tele_id) == 0:
#                     await bot.send_message(chat_id=tele_id,
#                                            text=text,
#                                            reply_markup=links(
#                                                message=message_link,
#                                                chat_id=int(
#                                                    str(event.chat_id)[4:]),
#                                                user=f"https://t.me/{username}"))
#                 if db.get_status(tele_id) == 1 and db.is_pay(tele_id):

#                     if chat.username is None:
#                         await bot.send_message(chat_id=tele_id,
#                                                text=text,
#                                                reply_markup=links(
#                                                    message=message_link,
#                                                    chat_id=int(
#                                                        str(event.chat_id)[4:]),
#                                                    user=f"t.me/{username}"))
#                     else:
#                         await bot.send_message(chat_id=tele_id,
#                                                text=text,
#                                                reply_markup=links(
#                                                    message=message_link,
#                                                    chat_id=f"{chat.username}",
#                                                    user=f"t.me/{username}"))
#         await connect_(event)


# async def connect_(event):
#     if '/request' in event.message.to_dict()['message']:
#         message = event.message.to_dict()['message'].split(" ")
#         telegram_id = message[-1]
#         urls = message[1].split("\n")

#         for url in message:
#             if 'http' in url:
#                 url.replace("\n", '')
#                 a = await join_(message, url, telegram_id)
#             else:
#                 pass
#                 for url in urls:
#                     a = await join_(message, url, telegram_id)
#                     await sleep(60)
#             await sleep(60)


# async def join_(message, url, telegram_id):
#     while True:
#         clear_url = str(url).replace('https://t.me/', '').replace("+",
#                                                                   "").replace('joinchat/', "")
#         try:
#             print("try")
#             await client(ImportChatInviteRequest(clear_url))
#             print("try")
#             await save(telegram_id, url, clear_url)
#             print("Joined and save", url)

#             return "true"
#         except InviteHashExpiredError:
#             try:
#                 entity = await client.get_entity(clear_url)
#                 await client(JoinChannelRequest(entity))
#                 await save(telegram_id, url, clear_url)
#                 print("Joined and save", url)
#                 await sleep(30)
#                 return
#             except ValueError:
#                 print("Ссылка недействительна!")
#                 await bot.send_message(
#                     chat_id=telegram_id, text=f"Ссылка на чат {url} недействительна... Попробуйте другую")
#                 return
#             except InviteRequestSentError:
#                 return
#             except ChannelsTooMuchError:
#                 await bot.send_message(chat_id=5909883622, text=f"/request {url} {message[-1]}")
#                 return
#             except FloodWaitError as ex:
#                 print(ex)
#                 print("Пересылаю")
#                 # await bot.send_message(chat_id=message[-1], text="Пересылаю")
#                 await bot.send_message(chat_id=5909883622, text=f"/request {url} {message[-1]}")
#                 return
#             except Exception as ex:
#                 print(ex)
#                 return
#         except (UserAlreadyParticipantError, InviteRequestSentError) as er:
#             print(er, url)
#             return
#         except FloodWaitError as ex:
#             print(ex)
#             print("Пересылаю")
#             await bot.send_message(chat_id=5909883622, text=f"/request {url} {message[-1]}")
#             return
#         except ValueError:
#             print("Ссылка недействительна!")
#             await bot.send_message(
#                 chat_id=telegram_id, text=f"Что-то пошло не так{url}")
#             return
#         except ChannelsTooMuchError:
#             await bot.send_message(chat_id=5909883622, text=f"/request {url} {message[-1]}")
#             return
#         except:
#             await bot.send_message(chat_id=5909883622, text=f"/request {url} {message[-1]}")
#             return
#         finally:
#             await sleep(5)


# async def save(telegram_id, url, clear_url):
#     while True:
#         try:
#             chat = await client.get_entity(clear_url)
#             await db.add_chat(telegram_id, clear_url, chat.id, chat.title)
#             print(f"Succes add chat {clear_url}")
#             sleep(30)
#             return
#         except ValueError as ex:
#             print(ex)
#             return
#         # except :
#         #     pass
#         except Exception as ex:
#             print(ex)

#         finally:
#             # sleep(60)
#             pass

with client:
    client.loop.run_until_complete(main())
# if __name__ == "__main__":
# print("Клиент запущен")
# client.start()
# run(a())
# client.run_until_disconnected()
