from email.utils import parseaddr
from typing import Optional, Tuple


class Validator:
    """
    Base validator class
    """

    async def validate(self, value) -> bool:
        return True


class ChoicesValidator(Validator):
    _choices: Optional[Tuple[str, str]] = None

    def __init__(self, choices: Optional[Tuple[Tuple[str, str]]] = None, *args, **kwargs):
        self._choices = choices
        super().__init__(*args, **kwargs)

    async def validate(self, value) -> bool:
        return value in {x[0] for x in self._choices}


class EmailValidator(Validator):

    async def validate(self, value) -> bool:
        return self._validate_email(value)

    @staticmethod
    def _validate_email(value) -> bool:
        _, email = parseaddr(value)
        return value == email
