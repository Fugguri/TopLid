from DB_connectors.MySql_connect import Database
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import InviteHashExpiredError, InviteRequestSentError, FloodWaitError, UserAlreadyParticipantError, ChannelsTooMuchError
from aiogram.utils.exceptions import MessageIsTooLong

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


def main(client):
    asyncio.run(work(client))




async def message(event):
    if event.chat_id == 777000:
        print(event)
    if not event.is_channel or not event.is_group:    
        return
    
    try:
        username = await event.get_sender()
        group = await event.get_chat()
    except:
        return

    keywords = db.all_words_()
    unex_words = db.all_unex_words_()
    final_words = []
    final_unex_words = []
    message_text = event.message.to_dict()['message']
    message_link = f't.me/c/{str(event.chat_id)[4:]}/{event.message.id}'
    chat_id = int(str(event.chat_id)[4:])
    print(chat_id)
    for word in keywords:
        if word.lower() in message_text.lower():
            final_words.append(word)
        if final_words == []:
            return

    for word in unex_words:
        if word.lower() in message_text.lower():
                final_unex_words.append(word)

    users = db.mailing_users(final_words, final_unex_words)
    text = f"""{message_text}\n""" +\
        "------------------------------\n" +\
        """\nЧтобы получить доступ к сообщению - нужно состоять в группе, или просто войти в группу (чтобы сообщения в группе прогрузились) и выйти. 
Только после этого будет доступна ссылка на сообщение."""

    for tele_id in users:
        is_all_chats = db.get_status(tele_id)
        is_pay = db.is_pay(tele_id)
        users_chat = db.all_mail_user_chats(tele_id)
        if not is_pay:
            return
        try:
            chat_id = "https://t.me/" + db.get_chat_link(chat_id)
        except:
            chat_id = "https://t.me/" + str(group.username)
            if not group.username:
                chat_id = "https://t.me/" + str(chat_id)
        try:
            usern = "t.me/"+username.username
        except:
            usern = "tg://user?id=" + str(username.id)
          
        if not is_all_chats and chat_id in users_chat:
            try:
                await bot.send_message(chat_id=tele_id,
                                    text=text,
                                    reply_markup=links(
                                       message=message_link,
                                       chat_id=chat_id,
                                       user=f"{usern}"))
            except MessageIsTooLong:
                pass
            except BotBlocked:
                print("Bot blocked by {}".format(chat_id))
                pass
            except Exception as ex:
                print(tele_id,ex)
        if is_all_chats:
            try:
                await bot.send_message(chat_id=tele_id,
                                    text=text,
                                    reply_markup=links(
                                       message=message_link,
                                       chat_id=chat_id,
                                       user=f"{usern}"))
            except MessageIsTooLong:
                return
            except BotBlocked:
                print("Bot blocked by {}".format(chat_id))
                pass
            except Exception as ex:
                print(tele_id,ex)


async def work(client):
    async with client:
        try:
            me = await client.get_me()
            print('Working with', me.first_name, me.last_name,me.phone)
            await client.start()
            client.add_event_handler(message, events.NewMessage)
            await client.run_until_disconnected()
        except Exception as ex:
            print(ex)

async def main():
    await asyncio.gather(
        work(client),
        work(client2),
        work(client3),
    )
    



if __name__ == "__main__":
    print("Клиент запущен")
        # try:
    asyncio.run(main())
        # except Exception as ex:
        #     print(ex)
        #     break
