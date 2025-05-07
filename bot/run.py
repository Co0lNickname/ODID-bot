import asyncio
from logging import getLogger

from aiogram.dispatcher.middlewares.error import CancelHandler

from bot.ODID_bot import run

logger = getLogger(__name__)


def main():
    try:
        asyncio.run(run())
    except CancelHandler as cancel:
        logger.error(f'cancel handler error: {cancel}')


if __name__ == '__main__':
    main()