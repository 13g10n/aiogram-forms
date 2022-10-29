"""
This example show usage of all available built-in field types.

Before run, make sure you set 'BOT_TOKEN' environment variable.
"""
import asyncio
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram_forms import dispatcher

from aiogram_forms.forms import Form
from aiogram_forms.forms.fields import TextField, SelectField

from aiogram_forms.menus import Menu, MenuItem


router = Router()


@dispatcher.register('test-form')
class TestForm(Form):
    name = TextField('Name')
    lang = SelectField('Language', choices=['English', 'Russian'])


@dispatcher.register('test-menu')
class TestMenu(Menu):
    form = MenuItem('Start form', action='test-form')
    settings = MenuItem('Settings')
    about = MenuItem('About')


@router.message(Command(commands=['start']))
async def command_start(message: Message, state: FSMContext) -> None:
    await dispatcher.show('test-form', message, state)


@router.message(Command(commands=['menu']))
async def command_menu(message: Message, state: FSMContext) -> None:
    await dispatcher.show('test-menu', message, state)


async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    dispatcher.attach(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
