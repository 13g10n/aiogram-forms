"""
This example show usage of all available built-in field types.

Before run, make sure you set 'BOT_TOKEN' environment variable.
"""
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram_forms import forms, fields, validators

from examples.base import dp, show_form_data

LANGUAGE_CHOICES = ('English', 'Russian', 'Chinese')
LANGUAGE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(*[
    KeyboardButton(label) for label in LANGUAGE_CHOICES
])


class UserProfileForm(forms.Form):
    """Example of user details form."""

    # Simple field usage
    name = fields.StringField('Name')
    # Using generic validator with custom error message
    username = fields.StringField(
        'Username', validators=[
            validators.RegexValidator(
                r'^[a-z0-9_-]{3,15}$',
                error_message='Username should be 3 to 15 lowercase symbols!'
            )
        ]
    )
    # Custom reply keyboard with validation
    language = fields.ChoicesField(
        'Language', LANGUAGE_CHOICES, reply_keyboard=LANGUAGE_KEYBOARD
    )
    email = fields.EmailField('Email')
    # Allow user to share contact as reply
    phone = fields.PhoneNumberField(
        'Phone', share_contact=True, share_contact_label='Share your contact'
    )


@dp.message_handler(commands="start")
async def command_start(message: types.Message):  # pylint: disable=unused-argument
    """Start form processing."""
    await UserProfileForm.start(callback=show_form_data, callback_args=(UserProfileForm, ))


@dp.message_handler(commands="info")
async def command_info(message: types.Message):  # pylint: disable=unused-argument
    """Show collected form data."""
    await show_form_data(UserProfileForm)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
