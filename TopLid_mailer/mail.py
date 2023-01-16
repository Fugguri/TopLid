from telethon.sync import TelegramClient, events
from asyncio import sleep

api_id = 28584421
api_hash = 'a65b42072ccdfa8301b97ffb497d0388'
phone = '+79502213750'
timer = 1  # TIME TO WAIT BEFORE NEXT SENDING
msgtosend = """Сообщение рассылки"""  # MESSAGE TO SEND
API_TOKEN = "5876350183:AAFMZZMvszFV06f2ZkG6qP5LyY1fpbUNrf4"

client = TelegramClient(phone, api_id, api_hash)
users_list = []
message = ""


def message(event):
    if "/message" in event.raw_text:
        return True
    else:
        return False


def users(event):
    if "/users" in event.raw_text:
        return True
    else:
        return False


def mail(event):
    if "/mail" in event.raw_text:
        return True
    else:
        return False


@client.on(events.NewMessage(incoming=True, func=message))
async def message(event):
    global message
    message = event.raw_text.replace("/message", "")
    await client.send_message(event.from_id, message="Успешно")


@client.on(events.NewMessage(incoming=True, func=users))
async def message(event):
    global users_list
    users_list = event.raw_text.replace("/users ", "").split(", ")
    await client.send_message(event.from_id, message="Успешно")


@client.on(events.NewMessage(incoming=True, func=mail))
async def message(event):
    global users_list
    global message
    for user in users_list:
        await client.send_message(user, message=message)
        await sleep(1)

if __name__ == "__main__":
    client.connect()
    client.run_until_disconnected()
