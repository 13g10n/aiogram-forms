from typing import Type, List, Callable

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message


class Field:
    _form: Type['Form'] = None
    _key: str = None
    _state = None

    _validators = None

    def __init__(
            self,
            name: str,
            validators: List[Callable] = None
    ):
        self.name = name
        self._validators = validators or []

    def __set_name__(self, owner: Type['Form'], name: str):
        if self._key is None:
            self._key = name
        self._form = owner

    @property
    def promotion(self):
        return self.name

    @property
    def state(self):
        return self._state

    @property
    def state_label(self):
        return f'waiting_{self._key}'

    @property
    def data_key(self):
        return f'{self._form._name}:{self._key}'

    def validate(self, value):
        for validator in self._validators:
            if not validator(value):
                return False
        return True
