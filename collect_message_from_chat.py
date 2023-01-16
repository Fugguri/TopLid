from datetime import date, datetime
from main import logger


async def get_message_history_by_keywords(chat_id, user_id, db, end_date_message):
    from HearBot2 import clients
    for client in clients:
        print("try")
        async with client:
            try:
                a = await client.get_entity(int(chat_id))
                print(a)
                await mes(chat_id, client, user_id, db, end_date_message)
                return
            except Exception as ex:
                print(ex)
    return


async def mes(chat_id, client, user_id, db, end_date_message):
    getmessage = client.iter_messages(int(chat_id))
    keywords = db.all_words(user_id)
    unex_words = db.all_unex_words(user_id)
    end_date = datetime.strptime(
        end_date_message, '%Y-%m-%d').timestamp()
    with open(f"chats/{chat_id}.txt", "w") as w:
        async for message in getmessage:
            if message.date.timestamp() < end_date:
                return
            elif message.message != None:

                key = any(
                    list(map(lambda x: x in message.message, keywords)))
                unex = any(
                    list(map(lambda x: x in message.message, unex_words)))
                if key and not unex:
                    sender = await message.get_sender()
                    mes = "\n"+str(message.date)[:-15] + "\n" + \
                        message.message + "\n" +\
                        f"\nДанные отправителя: \nid: {sender.id}, \nИмя: {sender.first_name}, \nФамилия: {sender.last_name}, \nUsername для поиска: {sender.username}" +\
                        f"\n\n Возможная ссылка на пользователя: t.me/{sender.username} \nЕсли в ссылке есть 'None' у пользователя нет username и телеграм не даст получить ссылку на него. \nМожно использовать парсеры для рассылки которые могут отправить сообщение по ID" +\
                        "\n\n - ------------------------------- \n"
                    w.write(mes)
                    logger.debug(mes)
        return
