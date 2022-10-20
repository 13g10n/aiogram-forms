"""
Fields of different types to handle different
user input and validate values
"""
from typing import Iterable, Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from aiogram_forms import validators
from aiogram_forms.base import BaseField
from aiogram_forms.const import EMAIL_REGEXP, PHONE_NUMBER_REGEXP


class StringField(BaseField):
    """String field."""


class ChoicesField(StringField):
    """Choices field."""
    _choices: Iterable[str] = None

    def __init__(self, label: str, choices: Iterable[str], *args, **kwargs) -> None:
        """
        Choices field.

        :param label: Field name
        :param choices: Iterable with available options to choice from
        """
        super().__init__(label, *args, **kwargs)
        self._validators.append(validators.ChoicesValidator(choices))


class EmailField(StringField):
    """Email field."""

    def __init__(self, label: str, *args, **kwargs) -> None:
        """
        Email field.

        :param label: Field name
        """
        super().__init__(label, *args, **kwargs)
        self._validators.append(validators.RegexValidator(EMAIL_REGEXP))


class PhoneNumberField(StringField):
    """Phone number field."""

    def __init__(
            self,
            label: str,
            *args,
            share_contact: bool = False,
            share_contact_label: Optional[str] = None,
            **kwargs
    ) -> None:
        """
        Phone number field.

        :param label: Field name
        :param share_contact: Show contact auto-sharing button
        :param share_contact_label: Text on the contact auto-sharing button
        """
        super().__init__(label, *args, **kwargs)
        self._validators.append(validators.RegexValidator(PHONE_NUMBER_REGEXP))

        if share_contact:
            self._reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
                KeyboardButton(share_contact_label or label, request_contact=True)
            )
