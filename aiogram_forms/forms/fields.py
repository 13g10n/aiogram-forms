"""
Form fields.
"""
from typing import Optional

from aiogram import types

from .base import Field
from . import validators


class TextField(Field):
    """Simple text field."""

    def __init__(self, *args, min_length: Optional[int] = None, max_length: Optional[int] = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(max_length))


class EmailField(Field):
    """Email field."""

    def __init__(self, label, *args, **kwargs) -> None:
        super().__init__(label, *args, **kwargs)
        self.validators.append(validators.EmailValidator())


class PhoneNumberField(Field):
    """Phone number field."""

    def __init__(self, label, *args, share_contact: Optional[bool] = False, **kwargs) -> None:
        super().__init__(label, *args, **kwargs)
        self.share_contact = share_contact
        self.validators.append(validators.PhoneNumberValidator())

    @property
    def reply_keyboard(self):
        if self.share_contact:
            return types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text=self.label, request_contact=True)]
                ],
                resize_keyboard=True
            )
        return super().reply_keyboard

    async def extract(self, message: types.Message) -> str:
        if message.content_type == 'contact':
            return message.contact.phone_number
        return await super().extract(message)
