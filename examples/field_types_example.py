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

# TODO: make it pretty
from aiogram_forms.dispatcher import dispatcher

from aiogram_forms.forms import forms, fields, validators

from aiogram_forms.menus import menus
from aiogram_forms.middleware import FormsManager

router = Router()


@dispatcher.register('test-form')
class TestForm(forms.Form):
    name = fields.TextField('Name')
    # username = fields.TextField(
    #     'Username', validators=[
    #         validators.RegexValidator(
    #             r'^[a-z0-9_-]{3,15}$',
    #             error_message='Username should be 3 to 15 lowercase symbols!'
    #         )
    #     ]
    # )
    # language = fields.SelectField('Language', choices=['English', 'Russian'])
    # email = fields.EmailField('Email')
    # phone = fields.PhoneNumberField('Phone')


@dispatcher.register('test-menu')
class TestMenu(menus.Menu):
    form = menus.MenuItem('Start form', action='test-form')
    settings = menus.MenuItem('Settings')
    about = menus.MenuItem('About')


@router.message(Command(commands=['start']))
async def command_start(message: Message, state: FSMContext, forms: 'FormsManager') -> None:
    # TODO: callback, callback_args
    await forms.show('test-form')


@router.message(Command(commands=['menu']))
async def command_menu(message: Message, state: FSMContext, forms: 'FormsManager') -> None:
    await forms.show('test-menu')


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
