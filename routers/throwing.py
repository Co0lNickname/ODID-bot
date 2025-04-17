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
async def throw_handler(message: types.Message, group_members_map: dict):
    action = random.choice(throw_actions)
    name = message.from_user.first_name
    sequence_number = group_members_map[message.chat.id][message.from_user.id]
    result_message = f"{name} ({sequence_number})\n\n🎲 {action}"
    await message.delete()
    await message.answer(result_message, parse_mode=ParseMode.MARKDOWN)
