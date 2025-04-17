import random

import structlog
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from routers.throwing import router as throwing_router
from keyboards.for_throwing import throw_keyboard_button
from settings import telegram_bot_token

logger = structlog.get_logger(__name__)

odid_bot = Bot(token=telegram_bot_token)
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)


@dispatcher.message(Command('start'))
async def start_handler(message: types.Message, group_members_map: dict):
    chat_id = message.chat.id
    members = await odid_bot.get_chat_administrators(chat_id)
    users = [member.user.id for member in members]
    random.shuffle(users)
    group_members_map[chat_id] = {user_id: index + 1 for index, user_id in enumerate(users)}
    await message.answer(
        f"""
        👋 Привет! Ваши порядковые номер: {
            [await odid_bot.get_chat_member(chat_id, member_id) for member_id in group_members_map[chat_id]]
        }
        """,
        reply_markup=throw_keyboard_button()
    )


async def run():
    """
    Main loop functions for polling telegram bot
    """
    dispatcher.include_routers(
        throwing_router,
    )

    await odid_bot.delete_webhook(
        drop_pending_updates=True
    )

    await dispatcher.start_polling(
        odid_bot,
        group_members_map={}
    )