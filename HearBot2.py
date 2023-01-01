from asyncio import sleep
import time
from telethon import TelegramClient, events
from telethon.tl.types import User, Channel, Chat as User, Channel, Chat
from telethon.events import *
from DB_connectors.MySql_connect import Database
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, ExportChatInviteRequest, CheckChatInviteRequest
from main import bot
from keyboards import links
from config import *
from telethon.tl.types import MessageActionContactSignUp, UpdateNewMessage
from telethon.errors.rpcerrorlist import InviteHashExpiredError, InviteRequestSentError, FloodWaitError, UserAlreadyParticipantError, ChannelsTooMuchError
import asyncio
from aiogram.utils.exceptions import BotBlocked
from pymysql.err import IntegrityError

db = Database('TopLid')
client = TelegramClient(phone, api_id, api_hash)
client2 = TelegramClient(phone2, api_id2, api_hash2)
client3 = TelegramClient(phone3, api_id3, api_hash3)
clients_id = [5593323077, 248184623]
clients = [client, client3]


def main(client):
    asyncio.run(work(client))


async def message(event):
    if '/request' not in event.message.to_dict()['message']:
        if event.is_channel or event.is_group:
            bot_id = event.original_update.message.peer_id.channel_id
            username = await event.get_sender()
            keywords = db.all_words_()
            unex_words = db.all_unex_words_()
            final_words = []
            final_unex_words = []
            for word in keywords:
                if word.lower() in event.message.to_dict()['message'].lower():
                    final_words.append(word)
            for word in unex_words:
                if word.lower() in event.message.to_dict()['message'].lower():
                    final_unex_words.append(word)
            if final_words != [] and bot_id != 5751517728:

                message_id = event.message.id
                users = db.mailing_users(final_words, final_unex_words)

                text = f"""{event.message.to_dict()['message']}"""
                message_link = f't.me/c/{str(event.chat_id)[4:]}/{message_id}'
                chat_id = int(str(event.chat_id)[4:])
                for tele_id in users:

                    try:
                        if int(str(event.chat_id)[4:]) in db.all_chats(tele_id) and db.is_pay(tele_id) and db.get_status(tele_id) == 0:
                            await bot.send_message(chat_id=tele_id,
                                                   text=text,
                                                   reply_markup=links(
                                                       message=message_link,
                                                       chat_id=срфе,
                                                       user=f"https://t.me/{username}"))
                        if db.get_status(tele_id) == 1 and db.is_pay(tele_id):
                            try:
                                if username.bot == False and username.username:
                                    await bot.send_message(chat_id=tele_id,
                                                           text=text,
                                                           reply_markup=links(
                                                               message=message_link,
                                                               chat_id=int(
                                                                   str(event.chat_id)[4:]),
                                                               user=f"t.me/{username.username}"))
                                # else:
                                #     await bot.send_message(chat_id=tele_id,
                                #                            text=text,
                                #                            reply_markup=links(
                                #                                message=message_link,
                                #                                chat_id=f"{username.username}",
                                #                                user=f"t.me/{username}"))
                            except:
                                pass
                            await sleep(0.5)
                    except BotBlocked:
                        pass


async def work(client):
    async with client:
        me = await client.get_me()
        # clients_id.append(me.id)
        print('Working with', me.first_name, me.last_name)
        print(clients_id, me.id)

        await client.start()

        @client.on(events.NewMessage)
        async def connect_(event):
            if '/request' in event.message.to_dict()['message']:
                message = event.message.to_dict()['message'].split(" ")
                telegram_id = message[-1]
                urls = [i.strip() for i in message[1].split("\n") if i != " "]
                print(message, telegram_id, urls)
                for url in message:
                    if 'http' in url:
                        url.replace("\n", '')
                        a = await join_chat(message, url, telegram_id, client)
                        await sleep(60)
                        return
                    else:
                        for url in urls:
                            await join_chat(message, url, telegram_id, client)
                            await sleep(60)

            return

        async def join_chat(message, url, telegram_id, client):
            while True:
                clear_url = str(url).replace('https://t.me/', '').replace("+",
                                                                          "").replace('joinchat/', "")
                try:
                    print("try", clear_url)
                    await client(ImportChatInviteRequest(clear_url))
                    print("try save")
                    await save(telegram_id, url, clear_url)
                    print("Joined and save", url)
                    return
                except InviteHashExpiredError as ex:
                    # print(ex)
                    try:
                        # print("try")
                        entity = await client.get_entity(clear_url)
                        await client(JoinChannelRequest(entity))
                        await save(telegram_id, url, clear_url)
                        print("Joined and save", url)
                        await sleep(30)
                        return
                    except ValueError:
                        print("Ссылка недействительна!")
                        await bot.send_message(
                            chat_id=telegram_id, text=f"Ссылка на чат {url} недействительна... Попробуйте другую")
                        return
                    except InviteRequestSentError as er:
                        print(er, 123)
                        return
                    except ChannelsTooMuchError:
                        await bot.send_message(chat_id=5909883622, text=f"/request {url} {message[-1]}")
                        return
                    except FloodWaitError as ex:
                        print(ex)
                        print("Пересылаю")
                        me = await client.get_me()
                        index = clients_id.index(int(me.id)) + 1
                        print(index)
                        print(clients_id[index])

                        await bot.send_message(chat_id=message[-1], text="Пересылаю")
                        await bot.send_message(chat_id=clients_id[index], text=f"/request {url} {message[-1]}")
                        return
                    # except Exception as ex:
                    #     print(ex)
                    #     return
                except (UserAlreadyParticipantError, InviteRequestSentError) as er:
                    print(er, url)
                    return
                except FloodWaitError as ex:
                    print(ex)
                    print("Пересылаю")
                    me = await client.get_me()
                    index = clients_id.index(me.id) + 1
                    print(clients_id.index(me.id), index)

                    await bot.send_message(chat_id=message[-1], text="Пересылаю")
                    await bot.send_message(chat_id=clients_id[index], text=f"/request {url} {message[-1]}")
                    return
                except ValueError:
                    print("Ссылка недействительна!")
                    await bot.send_message(
                        chat_id=telegram_id, text=f"Что-то пошло не так {url}")
                    return
                except ChannelsTooMuchError:
                    print("Ограничение количества чатов")
                    me = await client.get_me()
                    index = clients_id.index(me.id)
                    print(clients_id.index(me.id))
                    await bot.send_message(chat_id=message[-1], text="Пересылаю")
                    await bot.send_message(chat_id=clients_id[index+1], text=f"/request {url} {message[-1]}")
                    return
                except:
                    me = await client.get_me()
                    index = clients_id.index(me.id)+1
                    print(clients_id.index(me.id))
                    await bot.send_message(chat_id=message[-1], text="Пересылаю")
                    await bot.send_message(chat_id=clients_id[index], text=f"/request {url} {message[-1]}")
                    return
                finally:
                    await sleep(5)

        async def save(telegram_id, url, clear_url):
            while True:
                try:
                    chat = await client.get_entity(clear_url)
                    db.add_chat(telegram_id, clear_url, chat.id, chat.title)
                    print(f"Succes add chat {clear_url}")
                    await sleep(30)
                    return
                except ValueError as ex:
                    print(ex)
                    return
                except IntegrityError:
                    return
                except Exception as ex:
                    print(ex)
                    return

        client.add_event_handler(message, events.NewMessage)
        # client.add_event_handler(connect_, events.NewMessage)
        await client.run_until_disconnected()


async def main():
    """     WARNING!!!
    add clients from bottom to top"""
    await asyncio.gather(
        # work(client3),
        work(client),
        # work(client2),
    )


# clt2 = Client(client2)
if __name__ == "__main__":
    print("Клиент запущен")
    asyncio.run(main())
