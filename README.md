# aiogram-forms
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram-forms)
![PyPI](https://img.shields.io/pypi/v/aiogram-forms)
![GitHub](https://img.shields.io/github/license/13g10n/aiogram-forms)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aiogram-forms?label=installs)

## Introduction
`aiogram-forms` is an addition for `aiogram` which allows you to create different forms and process user input step by step easily.

## Installation
```bash
pip install aiogram-forms
```

## Usage
Create form you need by subclassing `aiogram_forms.forms.Form`. Fields can be added with `aiogram_forms.fields.Field`. For more examples refer to `examples` folder.
```python
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
```

## History
All notable changes to this project will be documented in [CHANGELOG](CHANGELOG.md) file.

## Translating

1. Extract
```bash
pybabel extract --input-dirs=aiogram_forms --project=aiogram-forms --version=0.4.0 --copyright-holder="Ivan Borisenko" -o locales/aiogram_forms.pot
```

2. Create new language
```bash
pybabel init -i locales/aiogram_forms.pot -d locales -D aiogram_forms -l ru
```

2. Or update existing one
```bash
pybabel update -d locales -D aiogram_forms -i locales/aiogram_forms.pot
```

3. Compile
```bash
pybabel compile -d locales -D aiogram_forms
```
