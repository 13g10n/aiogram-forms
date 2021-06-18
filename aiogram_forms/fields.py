"""
Fields of different types to handle different
user input and validate values
"""
from typing import Optional, Iterable

from aiogram_forms import validators
from aiogram_forms.base import BaseField
from aiogram_forms.validators import ChoicesValidator


class StringField(BaseField):
    """
    Simple string field
    """
    _choices: Iterable[str] = None

    def __init__(self, *args, choices: Optional[Iterable[str]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        if choices:
            self._validators.append(ChoicesValidator(choices=choices))


class EmailField(StringField):
    """
    Email-formatted field
    """

    def __init__(self, label: str, *args, **kwargs):
        """
        Add email format validator to field
        :param label:
        :param args:
        :param kwargs:
        """
        kwargs['validators'] = kwargs.get('validators', []) + [validators.EmailValidator()]
        super().__init__(label, *args, **kwargs)
