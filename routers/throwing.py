import random

import structlog
from aiogram.filters import Command
from aiogram import Router, types, F, Bot
from aiogram.enums.chat_type import ChatType
from aiogram.enums.parse_mode import ParseMode

from constants import throw_actions
from filters.chat_type import ChatTypeFilter
from middlewares.admin_rules import AdminCheckMiddleware
from middlewares.ensure_starting import EnsureStartedMiddleware
from keyboards.for_throwing import throw_keyboard_button, confirm_participation_button

logger = structlog.get_logger(__name__)
router = Router()
router.message.filter(ChatTypeFilter(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP]))
router.message.middleware(AdminCheckMiddleware())
router.message.middleware(EnsureStartedMiddleware())


@router.message(Command('start'))
async def start_handler(message: types.Message, confirmed_participants: dict):
    chat_id = message.chat.id
    if chat_id not in confirmed_participants:
        confirmed_participants[chat_id] = set()
    
    await message.answer(
        "👋 Привет! Подтверди участие, нажав на кнопку ниже.\n\nЕсли хотите завершить расчет, нажмите /finish",
        reply_markup=confirm_participation_button()
    )

@router.message(lambda message: message.text == "Подтвердить участие")
async def confirm_handler(message: types.Message, confirmed_participants: dict):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if chat_id not in confirmed_participants:
        confirmed_participants[chat_id] = set()
    
    if user_id in confirmed_participants[chat_id]:
        await message.answer(
            f"❌ {message.from_user.first_name}, вы уже подтвердили участие!",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return
    
    confirmed_participants[chat_id].add(user_id)
    await message.answer(f"✅ {message.from_user.first_name}, ваше участие подтверждено!")

@router.message(Command('finish'))
async def finish_handler(
    message: types.Message,
    confirmed_participants: dict,
    group_members_map: dict,
    odid_bot: Bot
):
    chat_id = message.chat.id
    
    if chat_id not in confirmed_participants or not confirmed_participants[chat_id]:
        await message.answer("❌ Никто не подтвердил участие!")
        return
    
    participants = list(confirmed_participants[chat_id])
    random.shuffle(participants)
    
    if chat_id not in group_members_map:
        group_members_map[chat_id] = {}
    
    for index, user_id in enumerate(participants):
        group_members_map[chat_id][user_id] = index + 1
    
    result_message = "🎲 Результаты:\n\n"
    
    for user_id, number in group_members_map[chat_id].items():
        user = await odid_bot.get_chat_member(chat_id, user_id)
        user_name = user.user.first_name
        if user.user.last_name:
            user_name += f" {user.user.last_name}"
        result_message += f"{number}. {user_name}\n"
    
    await message.answer(result_message, reply_markup=throw_keyboard_button())
    
    confirmed_participants[chat_id] = set()


@router.message(F.text.lower() == 'бросок')
async def throw_handler(message: types.Message, group_members_map: dict):
    action = random.choice(throw_actions)
    name = message.from_user.first_name
    sequence_number = group_members_map[message.chat.id][message.from_user.id]
    result_message = f"{name} ({sequence_number})\n\n🎲 {action}"
    await message.delete()
    await message.answer(result_message, parse_mode=ParseMode.MARKDOWN)
