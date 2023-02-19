from asyncio import sleep
from datetime import date, timedelta
from keyboards import words_list, back, chats_list_, chats_key, message_collector_week_range
from aiogram.dispatcher.filters import Text
from aiogram import types
from main import dp, db, bot, logger
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils.collect_message_from_chat_client import get_message_history_by_keywords
from join_chat import connect_and_url_clean
from .collect_message_from_chat_bot import CollectMessage


class AddChat(StatesGroup):
    chat = State()


'''Чаты !!!'''


@ dp.message_handler(Text(equals='Удалить все чаты'))
async def unexcepted_keywords_list(message: types.Message):
    if db.is_pay(message.from_user.id) is False:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")
    else:
        db.delete_all(message.from_user.id, 'users_chats')
        await message.answer(text="Вы удалили все чаты.\n Не забудьте добавить новые!",
                             reply_markup=chats_list_(message.from_user.id))
        logger.debug(f"{message.from_user} Удаление всех чатов")


@ dp.message_handler(Text(equals="Собирать из всех чатов"))
async def all_chat_acces(message: types.Message):
    if db.is_pay(message.from_user.id):
        db.set_status(message.from_user.id, 1)
        await message.answer(text="Вы переключились на нашу базу чатов",
                             reply_markup=chats_list_(message.from_user.id))
        logger.debug(f"{message.from_user} Переключение базы чатов: наша база")
    else:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")
        logger.debug(f"{message.from_user} Ограничение подписки в чатах")


@ dp.message_handler(Text(equals="Собирать из моих чатов"))
async def all_chat_acces(message: types.Message):
    if db.is_pay(message.from_user.id):
        db.set_status(message.from_user.id, 0)
        await message.answer(text="Вы переключились собственный список чатов",
                             reply_markup=chats_list_(message.from_user.id))
        logger.debug(
            f"{message.from_user} Переключение базы чатов: база юзера")
    else:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые слова
Подписку можно приобрести по кнопке «оплата 💰»""")
        logger.debug(f"{message.from_user} Ограничение подписки в чатах")


@ dp.message_handler(Text(equals='Мои чаты'))
async def chatse_list(message: types.Message):
    keywords = db.all_user_chats(message.from_user.id)
    text = "Список ваших чатов!\nЧтобы удалить, нажмите на чат!"
    logger.debug(f"{message.from_user} получение списка чатов")
    try:
        await message.answer(text=str(text),
                             reply_markup=chats_key(keywords))
    except:
        text += 'Вы можете добавить чаты нажав на кнопку "Добавить чат"\nИли вы еще не добавляли чаты или произошла ощибка, обратитесь в поддержку в случае необходимости. '
        await message.answer(text=str(text))
        logger.debug(f"{message.from_user} Нет чатов или ошибка в отображении")


@ dp.message_handler(Text(equals='Добавить новый чат'))
async def add_word_menu(message: types.Message):
    if db.is_pay(message.from_user.id):
        await AddChat.chat.set()
        await message.answer(text="Введите ссылку на чат", reply_markup=back())
        logger.debug(f"{message.from_user} Добавление чата")
    else:
        await message.answer(text="""Ваш текущий уровень подписки не позволяет добавить вам новые чаты
Подписку можно приобрести по кнопке «оплата 💰»""")
        logger.debug(f"{message.from_user} Ограничение подписки в чатах")


@ dp.callback_query_handler(lambda call: call.data in list(map(lambda x: str(x[1]), db.all_user_chats(call['from']['id']))))
async def remove_chat(call: types.CallbackQuery):
    try:
        db.remove_chat(call['from']['id'], call.data)
        keywords = db.all_user_chats(call['from']['id'])
        await call.message.answer("Список ваших чатов!\nЧтобы удалить, нажмите на название чата!",
                                  reply_markup=chats_key(keywords))
        logger.debug(f"{call.from_user} Удаление чата {call.data}")
    except:
        await call.message.answer("Возникла ошибка, просьба сообщить о ней для улушчения качества работы бота.",
                                  reply_markup=chats_key(keywords))
        logger.debug(f"{call.from_user} Удаление чата {call.data} Ошибка")


@ dp.message_handler(Text(equals="Назад"), state=[AddChat, CollectMessage])
async def add_word(message: types.Message, state: State):
    await state.finish()
    await message.answer(text='Бот выполняет поиск по ключевым словам.\n'
                         'Вы можете задать / удалить слова и фразы, по которым будет осуществляться поиск в чатах в пункте меню\n"Добавить новые слова" ниже\n\n'
                         'Для того, чтобы поиск начал работать, не забудьте добавить чаты в меню “Чаты”, в которых нужно отслеживать ключевые слова.',
                         reply_markup=chats_list_(message.from_user.id))
    logger.debug(f"{message.from_user} Назад из добавление чатов")


@ dp.callback_query_handler(lambda call: call.data in list(map(lambda x: str(x[1]), db.all_user_chats(call['from']['id']))), state=AddChat.chat)
async def remove_chat(call: types.CallbackQuery):
    try:
        db.remove_chat(call['from']['id'], call.data)
        keywords = db.all_user_chats(call['from']['id'])
        await call.message.answer("Список ваших чатов!\nЧтобы удалить, нажмите на название чата!",
                                  reply_markup=chats_key(keywords))
        logger.debug(f"{call.from_user} Удаление чата {call.data}")
    except:
        await call.message.answer("Возникла ошибка, просьба сообщить о ней для улушчения качества работы бота.",
                                  reply_markup=chats_key(keywords))
        logger.debug(f"{call.from_user} Удаление чата {call.data} Ошибка")


# @ dp.callback_query_handler(lambda call: call.text in db.all_user_chats(call['from']['id']), state=AddChat.chat)
# async def remove_chat(call: types.CallbackQuery):
#     try:
#         db.remove_chat(call['from']['id'], call.data)
#         keywords = db.all_user_chats(call['from']['id'])
#         await call.message.answer("Список ваших чатов!\nЧтобы удалить, нажмите на название чата!",
#                                   reply_markup=chats_key(keywords))
#         logger.debug(f"{call.from_user} Удаление чата {call.text}")
#     except:
#         await call.message.answer("Возникла ошибка, просьба сообщить о ней для улушчения качества работы бота.",
#                                   reply_markup=chats_key(keywords))
#         logger.debug(f"{call.from_user} Удаление чата {call.text} Ошибка")


@ dp.message_handler(state=AddChat.chat)
async def add_word(message: types.Message):
    # await bot.send_message(chat_id=5593323077, text=f'/request {str(message.text)} {message.from_user.id}')
    await connect_and_url_clean(message, db)
    await sleep(1.5)
    logger.debug(f"{message.from_user} Добавление чата {message.text}")
    chats = db.all_user_chats(message.from_user.id)
    await message.answer(
        text="Ваши чаты. Добавленный чат отобразится через время, после того как бот вступит в чат.\nЧтобы удалить нажмите на название чата", reply_markup=chats_key(chats))
