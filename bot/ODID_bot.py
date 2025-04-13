import structlog
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from routers.throwing import router as throwing_router

logger = structlog.get_logger(__name__)

bot_token = ''
odid_bot = Bot(token=bot_token)
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
        odid_bot
    )