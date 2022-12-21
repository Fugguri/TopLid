from asyncio import sleep

from telethon import TelegramClient, events
from telethon.tl.types import User, Channel, Chat as User, Channel, Chat
from DB_connectors.MySql_connect import Database
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, ExportChatInviteRequest
from main import bot
from keyboards import links
from config import api_hash, api_id, phone
from telethon.tl.types import MessageActionContactSignUp, UpdateNewMessage
# api_id = 18377495
# api_hash = 'a0c785ad0fd3e92e7c131f0a70987987'
# phone = '89502213750'
db = Database('TopLid')

client = TelegramClient(phone, api_id, api_hash)


@client.on(events.NewMessage)
async def message(event):
    chat = await client.get_entity(event.chat_id)
    username = await event.get_sender()
    if chat is not User and chat.id != 5751517728:
        # print(event.message.to_dict()['message'])
        keywords = db.all_words_()
        unex_words = db.all_unex_words_()
        chat_username = chat.usernames
        message_id = event.message.id
        message_link = ""
        final_words = []
        final_unex_words = []
        text = f"""{event.message.to_dict()['message']}"""
        message_link = f't.me/c/{str(event.chat_id)[4:]}/{message_id}'

        try:
            username = username.username
        except:
            if username is not None:
                username = username.user_id
            else:
                username = None
        for word in keywords:
            if word.lower() in event.message.to_dict()['message'].lower():
                final_words.append(word)
        for word in unex_words:
            if word.lower() in event.message.to_dict()['message'].lower():
                final_unex_words.append(word)
        if final_words != []:
            if final_unex_words == []:
                final_unex_words == ['bcbcv', 'bvbcv']

        users = db.mailing_users(final_words, final_unex_words)
        for tele_id in users:
            if int(str(event.chat_id)[4:]) in db.all_chats(tele_id) and db.is_pay(tele_id) and db.get_status(tele_id) == 0:
                await bot.send_message(chat_id=tele_id,
                                       text=text,
                                       reply_markup=links(
                                           message=message_link,
                                           chat_id=int(str(event.chat_id)[4:]),
                                           user=f"https://t.me/{username}"))
            if db.get_status(tele_id) == 1 and db.is_pay(tele_id):

                if chat.username is None:
                    await bot.send_message(chat_id=tele_id,
                                           text=text,
                                           reply_markup=links(
                                               message=message_link,
                                               chat_id=int(
                                                   str(event.chat_id)[4:]),
                                               user=f"t.me/{username}"))
                else:
                    await bot.send_message(chat_id=tele_id,
                                           text=text,
                                           reply_markup=links(
                                               message=message_link,
                                               chat_id=f"{chat.username}",
                                               user=f"t.me/{username}"))
        await connect_(event)


async def connect_(event):
    if '/request' in event.message.to_dict()['message']:
        message = event.message.to_dict()['message'].split(" ")
        telegram_id = message[-1]
        urls = message[1].split("\n")
        print(urls)
        for url in urls:
            clear_url = str(url).replace('https://t.me/', '').replace("+",
                                                                      "").replace('joinchat/', "")
            print(url)
            try:
                entity = await client.get_entity(clear_url)

                await client(JoinChannelRequest(entity))
                print("Joined %s", url)
            except:
                await client(ImportChatInviteRequest(clear_url))
            else:
                pass
            finally:
                await save(telegram_id, url, clear_url)
            await sleep(5)


async def save(telegram_id, url, clear_url):
    while True:
        try:
            chat = await client.get_entity(clear_url)
            print(url, clear_url, chat.id, chat.title)

            db.add_chat(telegram_id, clear_url, chat.id, chat.title)
            print("Succesed add chat")
            return
        except Exception as ex:
            print(ex)
        finally:
            await sleep(60)


if __name__ == "__main__":
    print("Клиент запущен")
    client.start()
    client.run_until_disconnected()
