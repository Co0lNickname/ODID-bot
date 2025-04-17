from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.dispatcher.middlewares.error import CancelHandler


class EnsureStartedMiddleware(BaseMiddleware):
    def __init__(self, user_numbers: dict):
        self.user_numbers = user_numbers

    async def __call__(self, handler, event, data):
        if isinstance(event, types.Message):
            chat_id = event.chat.id
            user_id = event.from_user.id
            key = (chat_id, user_id)

            if key not in self.user_numbers:
                await event.answer("⚠️ Сначала введите /start, чтобы получить номер.")
                raise CancelHandler()

        return await handler(event, data)