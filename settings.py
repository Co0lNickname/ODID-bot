from os import environ
from enum import Enum

import structlog

logger = structlog.get_logger(__name__)


class Settings(Enum):
    TELEGRAM_BOT_TOKEN_KEY = environ.get('TELEGRAM_BOT_TOKEN_KEY', None)

    @staticmethod
    def to_string():
        string = ', '.join(f'{var.name} = {var.value}' for var in Settings)
        return f'({string})'

logger.info(
    'read environment variables',
    settings=Settings.to_string()
)

telegram_bot_token = Settings.TELEGRAM_BOT_TOKEN_KEY.value