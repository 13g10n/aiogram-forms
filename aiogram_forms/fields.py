from typing import Type, List, Optional, Tuple, TYPE_CHECKING

from aiogram_forms import validators

if TYPE_CHECKING:
    from aiogram_forms.forms import Form
    from aiogram_forms.validators import Validator


class Field:
    _form: Type['Form'] = None
    _key: str = None
    _state = None

    _label: str = None
    _validators: List['Validator'] = None

    def __init__(
            self,
            label: str,
            validators: List['Validator'] = None
    ):
        self._label = label
        self._validators = validators or []

    def __set_name__(self, owner: Type['Form'], name: str):
        if self._key is None:
            self._key = name
        self._form = owner

    @property
    def state(self):
        return self._state

    @property
    def label(self):
        return self._label

    @property
    def state_label(self):
        return f'waiting_{self._key}'

    @property
    def data_key(self):
        return f'{self._form._name}:{self._key}'

    async def validate(self, value):
        for validator in self._validators:
            if not await validator.validate(value):
                return False
        return True


class StringField(Field):
    def __init__(self, label: str, choices: Optional[Tuple[Tuple[str, str]]] = None, *args, **kwargs):
        if choices:
            kwargs['validators'] = kwargs.get('validators', []) + [validators.ChoicesValidator(choices=choices)]
        super().__init__(label, *args, **kwargs)


class EmailField(Field):
    def __init__(self, label: str, choices: Optional[Tuple[Tuple[str, str]]] = None, *args, **kwargs):
        if choices:
            kwargs['validators'] = kwargs.get('validators', []) + [validators.EmailValidator()]
        super().__init__(label, *args, **kwargs)
