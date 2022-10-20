"""
Basic setup for all examples.
"""
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
