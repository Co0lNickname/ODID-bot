import random

import structlog
from aiogram import Router, types, F
from aiogram.enums.parse_mode import ParseMode

from constants import throw_actions
from filters.chat_type import ChatTypeFilter
from middlewares.admin_rules import AdminCheckMiddleware
from middlewares.ensure_starting import EnsureStartedMiddleware

logger = structlog.get_logger(__name__)
router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))
router.message.middleware(AdminCheckMiddleware())
router.message.middleware(EnsureStartedMiddleware())


@router.message(F.text.lower() == 'бросок')
async def throw_handler(message: types.Message):
    action = random.choice(throw_actions)
    await message.delete()
    await message.answer(action, parse_mode=ParseMode.MARKDOWN)
