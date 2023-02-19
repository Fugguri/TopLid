from DB_connectors.MySql_connect import Database
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import InviteHashExpiredError, InviteRequestSentError, FloodWaitError, UserAlreadyParticipantError, ChannelsTooMuchError
from telethon.events import *
from aiogram.utils.exceptions import BotBlocked
from pymysql.err import IntegrityError
from keyboards import links
from config import *
from main import bot
from asyncio import sleep
import asyncio
import threading
db = Database('TopLid')
client = TelegramClient(f"sessions/{phone}", api_id, api_hash)
client2 = TelegramClient(f"sessions/{phone2}", api_id2, api_hash2)
client3 = TelegramClient(f"sessions/{phone3}", api_id3, api_hash3)
client4 = TelegramClient(f"sessions/{phone4}", api_id4, api_hash4)
client5 = TelegramClient(f"sessions/{phone5}", api_id5, api_hash5)
client6 = TelegramClient(f"sessions/{phone6}", api_id6, api_hash6)
client7 = TelegramClient(f"sessions/{phone7}", api_id7, api_hash7)
client8 = TelegramClient(f"sessions/{phone8}", api_id8, api_hash8)
client9 = TelegramClient(f"sessions/{phone9}", api_id9, api_hash9)
clients_id = [5593323077, 5486075758]
clients = [
    TelegramClient(f"sessions_for_bot/{phone}", api_id, api_hash),
    TelegramClient(f"sessions_for_bot/{phone4}", api_id4, api_hash4),
    TelegramClient(f"sessions_for_bot/{phone6}", api_id6, api_hash6),
    TelegramClient(f"sessions_for_bot/{phone9}", api_id9, api_hash9)
]


def main(client):
    asyncio.run(work(client))


keywords = db.all_words_()
unex_words = db.all_unex_words_()


async def message(event):

    if '/request' not in event.message.to_dict()['message']:
        if event.is_channel or event.is_group:
            try:
                bot_id = event.original_update.message.peer_id.channel_id
            except:
                pass

            username = await event.get_sender()
            group = await event.get_chat()
            final_words = []
            final_unex_words = []
            lover_message_text = event.message.to_dict()['message'].lower()
            message_id = event.message.id

            for word in keywords:
                if word.lower() + " " in lover_message_text:
                    final_words.append(word)

            for word in unex_words:
                if word.lower()+" " in lover_message_text:
                    final_unex_words.append(word)

            if final_words != []:

                users = db.mailing_users(final_words, final_unex_words)
                text = f"""{event.message.to_dict()['message']}\n""" +\
                    "------------------------------\n" +\
                    """\nЧтобы получить доступ к сообщению - нужно состоять в группе, или просто войти в группу (чтобы сообщения в группе прогрузились) и выйти. Только после этого будет доступна ссылка на сообщение."""
                message_link = f't.me/c/{str(event.chat_id)[4:]}/{message_id}'
                chat_id = int(str(event.chat_id)[4:])

                for tele_id in users:
                    user_status = db.get_status(tele_id)
                    is_pay = db.is_pay(tele_id)
                    users_chat = db.all_mail_user_chats(tele_id)
                    try:
                        if is_pay:
                            if user_status == 0 and chat_id in users_chat:

                                if username:

                                    try:
                                        chat_id = "https://t.me/" + \
                                            db.get_chat_link(chat_id)
                                    except:
                                        if group.username != None:
                                            chat_id = "https://t.me/" + \
                                                str(group.username)
                                        else:
                                            chat_id = "https://t.me/" + \
                                                str(chat_id)
                                    finally:
                                        try:
                                            usern = "t.me/"+username.username
                                        except:
                                            usern = "tg://user?id=" + \
                                                str(username.id)
                                        await bot.send_message(chat_id=tele_id,
                                                               text=text,
                                                               reply_markup=links(
                                                                   message=message_link,
                                                                   chat_id=chat_id,
                                                                   user=f"{usern}"))

                            if user_status == 1:

                                if username:

                                    try:
                                        chat_id = "https://t.me/" + \
                                            db.get_chat_link(chat_id)
                                    except:
                                        if group.username != None:
                                            chat_id = "https://t.me/" + \
                                                str(group.username)
                                        else:
                                            chat_id = "https://t.me/" + \
                                                str(chat_id)
                                    finally:
                                        try:
                                            usern = "t.me/"+username.username
                                        except:
                                            usern = "tg://user?id=" + \
                                                str(username.id)
                                        await bot.send_message(chat_id=tele_id,
                                                               text=text,
                                                               reply_markup=links(
                                                                   message=message_link,
                                                                   chat_id=chat_id,
                                                                   user=f"{usern}"))

                    except BotBlocked:
                        print("Bot blocked")
                        pass


async def work(client):
    async with client:
        me = await client.get_me()
        print('Working with', me.first_name, me.last_name)
        await client.start()
        client.add_event_handler(message, events.NewMessage)
        await client.run_until_disconnected()


async def main():
    # loop = asyncio.get_event_loop()
    # client.start()
    # client3.start()
    # client4.start()
    # client6.start()
    # client9.start()
    # loop.run_forever()
    pass


if __name__ == "__main__":
    print("Клиент запущен")
    # asyncio.run(main())
    asyncio.gather(
        work(client),
        work(client3),
        work(client4),
        work(client6),
        work(client9),
        # work(client7),
        # work(client8),
        # work(client5),
    )
