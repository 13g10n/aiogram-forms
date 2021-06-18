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

class UserForm(forms.Form):
    """User profile data form"""
    name = fields.StringField('Name')
    language = fields.StringField('Language', choices=('English', 'Russian', 'Chinese'))
    email = fields.EmailField('Email')
```

## Code of Conduct

## History
All notable changes to this project will be documented in [CHANGELOG](CHANGELOG.md) file.
