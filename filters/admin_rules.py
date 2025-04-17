from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.event.handler import CancelHandler
from aiogram.dispatcher import FSMContext


class AdminCheckMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user_id = update.message.from_user.id
            chat_id = update.message.chat.id
            member = await update.bot.get_chat_member(chat_id, user_id)
            if member.is_chat_admin():
                return
        raise CancelHandler()