import structlog
from aiogram import Router, types
from aiogram.filters import Command

logger = structlog.get_logger(__name__)
router = Router()

