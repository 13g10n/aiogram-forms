# aiogram-forms

## Introduction
`aiogram-forms` is an addition for `aiogram` which allows you to create different forms and process user input step by step easily.

## Installation
```bash
pip install aiogram-forms
```

## Usage
Create form you need by subclassing `aiogram_forms.Form`. Fields can be added with `aiogram_forms.Field` 
```python
import aiogram_forms

class UserForm(aiogram_forms.Form):
    """User profile data form"""
    first_name = aiogram_forms.Field('First name')
    last_name = aiogram_forms.Field('Last name')
    email = aiogram_forms.Field('Email', validators=[lambda value: '@' in value])
```

## Code of Conduct

## History
All notable changes to this project will be documented in [CHANGELOG](CHANGELOG.md) file.