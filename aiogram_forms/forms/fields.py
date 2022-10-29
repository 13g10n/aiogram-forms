from typing import List, Optional

from aiogram import types

from .base import Field, Validator
from .validators import ChoicesValidator


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
