from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.dispatcher.middlewares.error import CancelHandler
from aiogram.exceptions import TelegramBadRequest

class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        return await handler(event, data)

    async def on_pre_process_update(self, update: types.Update, data: dict):
        try:
            if update.message:
                user_id = update.message.from_user.id
                chat_id = update.message.chat.id
                member = await update.bot.get_chat_member(chat_id, user_id)
                if member.is_chat_admin():
                    return
            raise CancelHandler()
        except TelegramBadRequest as exception:
            if "message can't be deleted" in exception.message:
                await update.message.answer('Для полного функционирования выдайте мне права на редактирование')
            else:
                await update.message.answer('Произошла ошибка при обработке вашего запроса.')
