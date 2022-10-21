"""
Basic setup for all examples.
"""
import os
from typing import Type

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram_forms import forms

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


async def show_form_data(form: Type[forms.Form]) -> None:
    """
    Show collected form data.

    Please note, that data stored by key, not by label.
    """
    data = await form.get_data()
    await bot.send_message(
        chat_id=types.Chat.get_current().id,
        text='\n'.join([
            f'{field.label}: {data[field.data_key]}'
            for field in form.get_fields()
        ])
    )
