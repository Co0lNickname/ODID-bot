from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.dispatcher.middlewares.error import CancelHandler

from constants import BotTexts


class EnsureStartedMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, types.Message):
            group_members_map = data.get('group_members_map', {})
            chat_id = event.chat.id
            user_id = event.from_user.id
            
            text = event.text if event.text else ""
            
            if (
                text == "Подтвердить участие" 
                or text.startswith('/finish')
                or text.startswith('/start') 
            ):
                return await handler(event, data)
                
            if (
                chat_id not in group_members_map 
                or user_id not in group_members_map.get(chat_id, {})
            ):
                await event.answer(BotTexts.MiddlewaresTexts.EnsureStarted.CONFIRM_PARTICIPATION_FIRST_TEXT)
                raise CancelHandler()

        return await handler(event, data)