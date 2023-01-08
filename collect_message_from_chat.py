from datetime import date, datetime


async def get_message_history_by_keywords(chat_id, user_id, db, end_date_message):
    from HearBot2 import clients
    for client in clients:
        print("try")
        async with client:
            # try:
            await mes(chat_id, client, user_id, db, end_date_message)
            return
            # except:
            #     print('except')
    return


async def mes(chat_id, client, user_id, db, end_date_message):
    from telethon.types import User
    getmessage = client.iter_messages(chat_id)
    keywords = db.all_words(user_id)
    unex_words = db.all_unex_words(user_id)
    end_date = datetime.strptime(
        end_date_message[user_id], '%Y-%m-%d').timestamp()
    with open(f"chats/{chat_id}.txt", "w") as w:
        async for message in getmessage:
            if message.date.timestamp() < end_date:
                return
            elif message.message != None:
                sender = await message.get_sender()
                key = any(
                    list(map(lambda x: x in message.message, keywords)))
                unex = any(
                    list(map(lambda x: x in message.message, unex_words)))
                if key and not unex:
                    mes = "\n"+str(message.date)[:-15] + \
                        message.message + \
                        f"\nДанные отправителя: \nid: {sender}" +\
                        "\n - ------------------------------- \n"
                    w.write(mes)
        return
