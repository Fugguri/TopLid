from datetime import date, datetime
from main import logger
from asyncio import sleep


async def get_message_history_by_keywords(chat_id, user_id, db, end_date_message, keywords, unex_words):
    from HearBot2 import clients
    for client in clients:
        print("try")

        async with client:

            try:
                chat = await client.get_entity(int(chat_id))
                logger.debug(end_date_message, keywords,
                             unex_words, chat.title)
                await mes(chat_id, client, user_id, db, end_date_message, keywords, unex_words, chat.title)
                return
            except ConnectionError:
                chat = await client.get_entity(int(chat_id))
                logger.debug(end_date_message, keywords,
                             unex_words, chat.title)
                await mes(chat_id, client, user_id, db, end_date_message, keywords, unex_words, chat.title)


async def mes(chat_id, client, user_id, db, end_date_message, keywords, unex_words, chat):
    getmessage = client.iter_messages(int(chat_id))

    if keywords != None and keywords != []:
        print(1)
        keywords == keywords
    else:
        print(2)
        keywords = [i[0] for i in db.all_words(user_id)]
    if unex_words != None and unex_words != []:
        unex_words = unex_words
    else:
        unex_words = [i[0] for i in db.all_unex_words(user_id)]
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
                    try:
                        sender = await message.get_sender()
                        mes = f"\nЕсли в ссылке есть 'None' у пользователя нет username и телеграм не даст получить ссылку на него." +\
                            "Можно использовать парсеры для рассылки которые могут отправить сообщение по ID\n\n" +\
                            "\n"+str(message.date)[:-15] + "\n" +\
                            "Текст сообщения: "+message.message + "\n\n" +\
                            f"\nДанные отправителя: \nid: {sender.id}, \nИмя: {sender.first_name}, \nФамилия: {sender.last_name}, \nUsername для поиска: {sender.username}" +\
                            f"\nВозможная ссылка на пользователя: t.me/{sender.username}\n" +\
                            f"\nПатерн для рассылки - username, user id, access hash, name, group, group id: " +\
                            f"\n{sender.username}, {sender.id}, {sender.access_hash}, {sender.last_name} {sender.last_name}, {chat}, {chat_id}" +\
                            "\n\n - ------------------------------- \n"
                        w.write(mes)
                        logger.debug(mes)
                    except Exception as ex:
                        logger.debug(ex, sender)
        return
