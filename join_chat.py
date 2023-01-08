from asyncio import sleep
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import InviteHashExpiredError, InviteRequestSentError, FloodWaitError, UserAlreadyParticipantError, ChannelsTooMuchError
from pymysql.err import IntegrityError
from HearBot2 import clients
from main import bot, logger


async def connect_and_url_clean(message, db):
    telegram_id = message.from_user.id
    message = message.text.replace("\n", "").replace(",", "").replace(
        " ", '').replace("+", "").replace('joinchat/', "")
    urls = message.split("https://t.me/")
    client_index = 0
    joined_group_count = 0
    logger.debug(f"{urls}, {telegram_id}")
    for url in urls:
        if joined_group_count < 4:
            if url != "":
                client = clients[client_index]
                try:
                    async with client:
                        await join_chat(message, url, telegram_id, client, db)
                    joined_group_count += 1
                    await sleep(5)
                except FloodWaitError as ex:
                    if client_index != len(clients):
                        client_index += 1
                        async with clients[client_index] as client:
                            await join_chat(message, url, telegram_id, client, db)
                        joined_group_count = 1
                        await sleep(5)
                    elif client_index == len(clients):
                        sleep(ex.seconds)
                        client_index = 0
                        async with clients[client_index] as client:
                            await join_chat(message, url, telegram_id, client, db)
                        joined_group_count = 1
                except ChannelsTooMuchError:
                    client_index += 1
                    async with clients[client_index] as client:
                        await join_chat(message, url, telegram_id, client, db)
                        joined_group_count = 1
                    await sleep(5)

                except:
                    client_index += 1
                    async with clients[client_index] as client:
                        await join_chat(message, url, telegram_id, client, db)
                    joined_group_count = 1
                    await sleep(5)
                finally:
                    logger.debug(f"done {url}")
        else:
            joined_group_count = 0
            logger.debug("Добавлено 4 чата! Тайм- аут 400 секунд")
            await sleep(400)


async def join_chat(message, url, telegram_id, client, db):
    clear_url = url
    try:
        logger.debug("try ChatInvite" + clear_url)
        await client(ImportChatInviteRequest(clear_url))
        await sleep(10)
        logger.debug("try save")
        await save(telegram_id, url, clear_url)
        logger.debug("Joined and save", url)
        return
    except InviteHashExpiredError as ex:
        try:
            logger.debug("try JoinChannel")
            entity = await client.get_entity(clear_url)
            await client(JoinChannelRequest(entity))
            logger.debug("try save")
            await save(telegram_id, url, clear_url, client, db)
            logger.debug(f"Joined and save, {url}")
            return
        except ValueError:
            logger.debug("Ссылка недействительна!")
            await bot.send_message(
                chat_id=telegram_id, text=f"Ссылка на чат {url} недействительна... Попробуйте другую")
            return
        except InviteRequestSentError as er:
            logger.debug(er)
            return
        except ChannelsTooMuchError:
            logger.debug("Ограничение по количеству групп " + url)
            await bot.send_message(chat_id=248184623, text=f"Ограничение по количеству групп {client}")
            return
    except InviteRequestSentError as er:
        logger.debug(str(er)+url)
        logger.debug("try save")
        await save(telegram_id, url, clear_url, client, db)
        logger.debug(f"Joined and save, {url}")
        return
    except ValueError:
        logger.debug("Ссылка недействительна!")
        await bot.send_message(
            chat_id=telegram_id, text=f"Что-то пошло не так {url}")
        return
    except ChannelsTooMuchError:
        logger.debug("Ограничение количества чатов")
    except UserAlreadyParticipantError:
        logger.debug("try save")
        await save(telegram_id, url, clear_url, client, db)
        return


async def save(telegram_id, url, clear_url, client, db):
    while True:
        try:
            print(clear_url)
            try:
                chat = await client.get_entity(url)
            except:
                chat = await client.get_entity("telegram.me/joinchat/"+url)
            print(chat)
            db.add_chat(telegram_id, clear_url, chat.id, chat.title)
            logger.debug(f"Succes add chat {clear_url}")
            return
        except IntegrityError:
            logger.debug(f"exist {clear_url}")
            return
