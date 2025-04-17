import structlog
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from routers.throwing import router as throwing_router
from settings import telegram_bot_token

logger = structlog.get_logger(__name__)

odid_bot = Bot(token=telegram_bot_token)
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)


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
        bot=odid_bot,
        group_members_map={},
        confirmed_participants={}
    )