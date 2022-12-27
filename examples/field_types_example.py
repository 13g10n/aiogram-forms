"""
This example show usage of all available built-in field types.

Before run, make sure you set 'BOT_TOKEN' environment variable.
"""
import asyncio
import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_forms import dispatcher
from aiogram_forms.forms import Form, fields, FormsManager
from aiogram_forms.errors import ValidationError

router = Router()


def validate_username_format(value: str):
    """Validate username starts with leading @."""
    if not value.startswith('@'):
        raise ValidationError('Username should starts with "@".', code='username_prefix')


@dispatcher.register('test-form')
class TestForm(Form):
    username = fields.TextField('Username', min_length=4, validators=[validate_username_format],
                                error_messages={'min_length': 'Username must contain at least 4 characters!'})
    email = fields.EmailField('Email', help_text='We will send confirmation code.')
    phone = fields.PhoneNumberField('Phone number', share_contact=True)
    value = fields.TextField('Value')

    @classmethod
    async def callback(cls, message: types.Message, forms: FormsManager, **data) -> None:  # noqa
        data = await forms.get_data(TestForm)
        await message.answer(text=f'Thank you!\n{data}')


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
