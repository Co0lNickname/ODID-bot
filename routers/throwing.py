import structlog
from aiogram import Router, types
from aiogram.filters import Command

from constants import HELLO_TEXT

logger = structlog.get_logger(__name__)
router = Router()


@router.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer(HELLO_TEXT)
