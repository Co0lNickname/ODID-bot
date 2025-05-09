import structlog

from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from aiogram.enums.chat_type import ChatType
from aiogram.fsm.storage.memory import MemoryStorage

from constants import BotTexts
from routers.throwing import router as throwing_router
from filters.chat_type import ChatTypeFilter
from settings import telegram_bot_token

logger = structlog.get_logger(__name__)

odid_bot = Bot(token=telegram_bot_token)
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)


@dispatcher.message(Command('start'), ChatTypeFilter(chat_type=[ChatType.PRIVATE, ChatType.SENDER]))
async def start_handler(message: types.Message):
    await message.answer(BotTexts.NotInGroupMessages.HELLO_TEXT)


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
        odid_bot=odid_bot,
        group_members_map={},
    )