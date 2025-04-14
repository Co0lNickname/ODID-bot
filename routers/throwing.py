import random

import structlog
from aiogram import Router, types, F
from aiogram.filters import Command

from constants import HELLO_TEXT, throw_actions
from filters.chat_type import ChatTypeFilter
from keyboards.for_throwing import throw_keyboard_button

logger = structlog.get_logger(__name__)
router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))


@router.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer(HELLO_TEXT, reply_markup=throw_keyboard_button())


@router.message(F.text.lower() == 'бросок')
async def throw_handler(message: types.Message):
    action = random.choice(throw_actions)
    await message.answer(action)