from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.dispatcher.middlewares.error import CancelHandler


class EnsureStartedMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, types.Message):
            users_dict = data.get('group_members_map', {})
            chat_id = event.chat.id
            user_id = event.from_user.id
            key = (chat_id, user_id)

            if key not in users_dict:
                await event.answer("⚠️ Сначала введите /start, чтобы получить номер.")
                raise CancelHandler()

        return await handler(event, data)