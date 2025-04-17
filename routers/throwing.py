import random

import structlog
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramBadRequest

from constants import HELLO_TEXT, throw_actions
from filters.chat_type import ChatTypeFilter
from middlewares.admin_rules import AdminCheckMiddleware
from keyboards.for_throwing import throw_keyboard_button

logger = structlog.get_logger(__name__)
router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))


@router.message(Command('start'))
async def start_handler(message: types.Message):
    await message.reply(HELLO_TEXT, reply_markup=throw_keyboard_button())


@router.message(F.text.lower() == 'бросок')
@AdminCheckMiddleware()
async def throw_handler(message: types.Message):
    action = random.choice(throw_actions)
    try:
        await message.delete()
        await message.answer(action, parse_mode=ParseMode.MARKDOWN)
    except TelegramBadRequest as exception:
        if "message can't be deleted" in exception.message:
            await message.answer('Для полного функционирования выдайте мне права на редактирование')
