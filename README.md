# aiogram-forms

## Introduction
`aiogram-forms` is an addition for `aiogram` which allows you to create different forms and process user input step by step easily.

## Installation
```bash
pip install aiogram-forms
```

## Usage
Create form you need by subclassing `aiogram_forms.forms.Form`. Fields can be added with `aiogram_forms.fields.Field` 
```python
from aiogram_forms import forms, fields
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class UserForm(forms.Form):
    LANGUAGE_CHOICES = ('English', 'Russian', 'Chinese')
    LANGUAGE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(*[
        KeyboardButton(label) for label in LANGUAGE_CHOICES
    ])

    name = fields.StringField('Name')
    language = fields.ChoicesField('Language', LANGUAGE_CHOICES, reply_keyboard=LANGUAGE_KEYBOARD)
    email = fields.EmailField('Email')
```

## Code of Conduct

## History
All notable changes to this project will be documented in [CHANGELOG](CHANGELOG.md) file.
