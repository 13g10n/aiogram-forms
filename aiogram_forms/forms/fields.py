from typing import List, Optional

from aiogram import types

from .forms import Field, Validator
from .validators import ChoicesValidator, RegexValidator
from .const import PHONE_NUMBER_REGEXP, EMAIL_REGEXP


class TextField(Field):
    pass


class SelectField(Field):
    _choices: List[str]

    def __init__(
            self,
            label: str,
            choices: List[str],
            validators: Optional[List[Validator]] = None
    ) -> None:
        super().__init__(label, validators=(validators or []) + [ChoicesValidator(choices)])
        self._choices = choices

    @property
    def reply_keyboard(self):
        return types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text=choice)
                ] for choice in self._choices
            ],
            resize_keyboard=True
        )


class EmailField(Field):

    def __init__(self, label, *args, **kwargs) -> None:
        super().__init__(label, *args, **kwargs)
        self._validators.append(
            RegexValidator(
                EMAIL_REGEXP,
                error_message='Invalid email format!'
            )
        )


class PhoneNumberField(Field):

    def __init__(self, label, *args, **kwargs) -> None:
        super().__init__(label, *args, **kwargs)
        self._validators.append(
            RegexValidator(
                PHONE_NUMBER_REGEXP,
                error_message='Invalid phone format!'
            )
        )

    @property
    def reply_keyboard(self):
        return types.ReplyKeyboardMarkup(
            keyboard=[[
                types.KeyboardButton(text='Share contact', request_contact=True)
            ]],
            resize_keyboard=True
        )
