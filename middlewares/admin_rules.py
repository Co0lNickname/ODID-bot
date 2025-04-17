import logging

from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.dispatcher.middlewares.error import CancelHandler
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types.chat_member_administrator import ChatMemberAdministrator

logger = logging.getLogger(__name__)


class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            user_id = event.from_user.id
            chat_id = event.chat.id
            bot = event.bot

            try:
                member = await bot.get_chat_member(chat_id, user_id)
                if member.status not in ("administrator", "creator"):
                    try:
                        await event.answer("🚫 Команда доступна только администраторам.")
                    except TelegramBadRequest as e:
                        logger.warning(f"Ошибка при попытке отправить ответ: {e}")
                    raise CancelHandler()

                bot_id = (await bot.me()).id
                bot_member = await bot.get_chat_member(chat_id, bot_id)

                if isinstance(bot_member, ChatMemberAdministrator):
                    if not bot_member.can_delete_messages:
                        try:
                            await event.answer("⚠️ У бота нет прав на удаление сообщений. Пожалуйста, добавьте эти права.")
                        except TelegramBadRequest as e:
                            logger.warning(f"Ошибка при попытке отправить предупреждение: {e}")
                        raise CancelHandler()
                else:
                    try:
                        await event.answer("🚫 У бота нет прав администратора.")
                    except TelegramBadRequest as e:
                        logger.warning(f"Ошибка при попытке отправить предупреждение: {e}")
                    raise CancelHandler()

            except TelegramBadRequest as e:
                logger.error(f"Ошибка при проверке прав: {e}")
                try:
                    await event.answer("❌ Ошибка при проверке прав доступа.")
                except TelegramBadRequest as err:
                    logger.warning(f"Ошибка при попытке отправить сообщение об ошибке: {err}")
                raise CancelHandler()

        return await handler(event, data)
