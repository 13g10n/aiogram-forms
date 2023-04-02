# aiogram-forms
![PyPI](https://img.shields.io/pypi/v/aiogram-forms)
![GitHub](https://img.shields.io/github/license/13g10n/aiogram-forms)
![Project status](https://img.shields.io/pypi/status/aiogram-forms)
![Project code coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aiogram-forms?label=installs)

## Introduction
`aiogram-forms` is an addition for `aiogram` which allows you to create different forms and process user input step by step easily.

## Documentation
Documentation can be found [here](https://13g10n.com/en/docs/aiogram-forms).

## Installation
```bash
pip install aiogram-forms
```

## Usage
Create form you need by subclassing `aiogram_forms.forms.Form`. Fields can be added from `aiogram_forms.forms.fields` subpackage.
```python
from aiogram_forms import dispatcher
from aiogram_forms.forms import Form, fields, FormsManager
from aiogram_forms.errors import ValidationError

def validate_username_format(value: str):
    """Validate username starts with leading @."""
    if not value.startswith('@'):
        raise ValidationError('Username should starts with "@".', code='username_prefix')

@dispatcher.register('test-form')
class TestForm(Form):
    username = fields.TextField(
        'Username', min_length=4, validators=[validate_username_format],
        error_messages={'min_length': 'Username must contain at least 4 characters!'}
    )
    email = fields.EmailField('Email', help_text='We will send confirmation code.')
    phone = fields.PhoneNumberField('Phone number', share_contact=True)
    language = fields.ChoiceField('Language', choices=(
        ('English', 'en'),
        ('Russian', 'ru')
    ))

    @classmethod
    async def callback(cls, message: types.Message, forms: FormsManager, **data) -> None:
        data = await forms.get_data('test-form')  # Get form data from state
        await message.answer(
            text=f'Thank you, {data["username"]}!',
            reply_markup=types.ReplyKeyboardRemove()  # Use this for reset if last field contains keyboard
        )

router = Router()

@router.message(Command(commands=['start']))
async def command_start(message: types.Message, forms: FormsManager) -> None:
    await forms.show('test-form')  # Start form processing

async def main():
    dp = Dispatcher()
    dp.include_router(router)

    dispatcher.attach(dp)  # Attach aiogram to forms dispatcher 

    bot = Bot(...)
    await dp.start_polling(bot)
```

## History
All notable changes to this project will be documented in [CHANGELOG](CHANGELOG.md) file.
