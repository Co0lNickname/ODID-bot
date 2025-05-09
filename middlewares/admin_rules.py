import logging

from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.dispatcher.middlewares.error import CancelHandler
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types.chat_member_administrator import ChatMemberAdministrator

from constants import BotTexts, LoggingMessages

logger = logging.getLogger(__name__)


class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            user_id = event.from_user.id
            chat_id = event.chat.id
            bot = event.bot

            try:
                bot_id = (await bot.me()).id
                bot_member = await bot.get_chat_member(chat_id, bot_id)

                if isinstance(bot_member, ChatMemberAdministrator):
                    if not bot_member.can_delete_messages:
                        try:
                            await event.answer(BotTexts.MiddlewaresTexts.AdminCheck.NO_RULES_ADD_IT_TEXT)
                        except TelegramBadRequest as e:
                            logger.warning(LoggingMessages.AdminCheck.ERROR_DURING_SEND_WARNING.format(error=e))
                        raise CancelHandler()
                else:
                    try:
                        await event.answer(BotTexts.MiddlewaresTexts.AdminCheck.NO_ADMIN_RULES_TEXT)
                    except TelegramBadRequest as e:
                        logger.warning(LoggingMessages.AdminCheck.ERROR_DURING_SEND_WARNING.format(error=e))
                    raise CancelHandler()

            except TelegramBadRequest as e:
                logger.error(LoggingMessages.AdminCheck.ERROR_DURING_RULES_CHECK.format(error=e))
                try:
                    await event.answer(BotTexts.MiddlewaresTexts.AdminCheck.ERROR_DURING_RULES_CHECK_TEXT)
                except TelegramBadRequest as err:
                    logger.warning(LoggingMessages.AdminCheck.ERROR_DURING_SEND_WARNING.format(error=err))
                raise CancelHandler()

        return await handler(event, data)
