"""
This example show usage of all available built-in field types.

Before run, make sure you set 'BOT_TOKEN' environment variable.
"""
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram_forms import forms, fields, validators

from examples.base import bot, dp


LANGUAGE_CHOICES = ('English', 'Russian', 'Chinese')
LANGUAGE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(*[
    KeyboardButton(label) for label in LANGUAGE_CHOICES
])


class UserProfileForm(forms.Form):
    """Example of user details form."""

    # Simple field usage
    name = fields.StringField('Name')
    # Using custom validators
    username = fields.StringField(
        'Username', validators=[validators.RegexValidator(r'^[a-z0-9_-]{3,15}$')]
    )
    # Custom reply keyboard with validation
    language = fields.ChoicesField(
        'Language', LANGUAGE_CHOICES, reply_keyboard=LANGUAGE_KEYBOARD
    )
    # Custom validation message
    email = fields.EmailField(
        'Email', validation_error_message='Wrong email format!'
    )
    # Allow user to share contact as reply
    phone = fields.PhoneNumberField(
        'Phone', share_contact=True, share_contact_label='Share your contact'
    )


@dp.message_handler(commands="start")
async def command_start(message: types.Message):  # pylint: disable=unused-argument
    """Start form processing."""
    await UserProfileForm.start(callback=_show_info)


@dp.message_handler(commands="info")
async def command_info(message: types.Message):  # pylint: disable=unused-argument
    """Show collected form data."""
    await _show_info()


async def _show_info():
    """
    Show collected form data.

    Please note, that data stored by key, not by label.
    """
    data = await UserProfileForm.get_data()
    await bot.send_message(
        chat_id=types.Chat.get_current().id,
        text='\n'.join([
            f'{field.label}: {data[field.data_key]}'
            for field in UserProfileForm.get_fields()
        ])
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
