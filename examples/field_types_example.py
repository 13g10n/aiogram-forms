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

from aiogram_forms.forms import forms, fields, validators, manager

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

    @classmethod
    async def callback(cls, message: Message, state: FSMContext, *args, **kwargs) -> None:
        await message.answer('This is custom callback!')


@router.message(Command(commands=['start']))
async def command_start(message: Message, forms_manager: 'manager.FormsManager') -> None:
    await forms_manager.show('test-form')


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
