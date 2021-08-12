"""
Fields of different types to handle different
user input and validate values
"""
from typing import Iterable

from aiogram_forms import validators
from aiogram_forms.base import BaseField
from aiogram_forms.validators import ChoicesValidator


class StringField(BaseField):
    """
    Simple string field
    """


class ChoicesField(StringField):
    """
    String field with value from given list only
    """
    _choices: Iterable[str] = None

    def __init__(self, label: str, choices: Iterable[str], *args, **kwargs) -> None:
        super().__init__(label, *args, **kwargs)
        self._validators.append(ChoicesValidator(choices))


class EmailField(StringField):
    """
    Email-formatted field
    """

    def __init__(self, label: str, *args, **kwargs) -> None:
        """
        Add email format validator to field
        :param label:
        :param args:
        :param kwargs:
        """
        kwargs['validators'] = kwargs.get('validators', []) + [validators.EmailValidator()]
        super().__init__(label, *args, **kwargs)
