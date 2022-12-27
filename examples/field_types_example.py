"""
This example show usage of all available built-in field types.

Before run, make sure you set 'BOT_TOKEN' environment variable.
"""
import asyncio
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_forms import dispatcher
from aiogram_forms.forms import Form, fields, FormsManager

router = Router()


@dispatcher.register('test-form')
class TestForm(Form):
    name = fields.TextField('Name')
    text = fields.TextField('Email')
    value = fields.TextField('Value')


@router.message(Command(commands=['start']))
async def command_start(message: Message, forms: FormsManager) -> None:
    await forms.show('test-form')


async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    dispatcher.attach(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
