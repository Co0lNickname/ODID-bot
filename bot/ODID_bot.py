import random

import structlog
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from routers.throwing import router as throwing_router
from keyboards.for_throwing import throw_keyboard_button, confirm_participation_button
from settings import telegram_bot_token

logger = structlog.get_logger(__name__)

odid_bot = Bot(token=telegram_bot_token)
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)

# Используем словарь для хранения данных о пользователях
group_members_map = {}
# Словарь для отслеживания участников, подтвердивших участие
confirmed_participants = {}

@dispatcher.message(Command('start'))
async def start_handler(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in confirmed_participants:
        confirmed_participants[chat_id] = set()
    
    await message.answer(
        "👋 Привет! Подтверди участие, нажав на кнопку ниже.\n\nЕсли хотите завершить расчет, нажмите /finish",
        reply_markup=confirm_participation_button()
    )

@dispatcher.message(lambda message: message.text == "Подтвердить участие")
async def confirm_handler(message: types.Message):
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
    await message.answer(
        f"✅ {message.from_user.first_name}, ваше участие подтверждено!",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dispatcher.message(Command('finish'))
async def finish_handler(message: types.Message):
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
        group_members_map=group_members_map
    )