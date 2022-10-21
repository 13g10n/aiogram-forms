"""
This example show usage of translatable labels, error messages etc.

Refer to original aiogram example for i18n setup:
https://docs.aiogram.dev/en/latest/examples/i18n_example.html

Before run, make sure you set 'BOT_TOKEN' environment variable.
"""
from pathlib import Path

from aiogram import executor, types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from aiogram_forms import forms, fields

from examples.base import dp, show_form_data

I18N_DOMAIN = 'mybot'

BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
dp.middleware.setup(i18n)

_ = i18n.lazy_gettext


class TranslatedForm(forms.Form):
    """Example of user details form."""

    phone = fields.PhoneNumberField(
        _('Phone'),
        share_contact=True,
        share_contact_label=_('Share your contact')
    )


@dp.message_handler(commands="start")
async def command_start(message: types.Message):  # pylint: disable=unused-argument
    """Start form processing."""
    await TranslatedForm.start(callback=show_form_data, callback_args=(TranslatedForm, ))


@dp.message_handler(commands="info")
async def command_info(message: types.Message):  # pylint: disable=unused-argument
    """Show collected form data."""
    await show_form_data(TranslatedForm)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
