import structlog
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.greeting import router as greeting_router

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
        greeting_router,
    )

    await odid_bot.delete_webhook(
        drop_pending_updates=True
    )

    await dispatcher.start_polling(
        odid_bot,
        users_tokens={}
    )