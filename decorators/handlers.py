from aiogram.exceptions import TelegramBadRequest
from aiogram import types
from functools import wraps


def exception_handler_decorator(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        try:
            return await func(message, *args, **kwargs)
        except TelegramBadRequest as exception:
            if "message can't be deleted" in exception.message:
                await message.answer('Для полного функционирования выдайте мне права на редактирование')
            else:
                await message.answer('Произошла ошибка при обработке вашего запроса.')
    return wrapper
