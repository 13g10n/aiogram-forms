"""
User input validators.
"""
import re
from typing import Optional, Iterable, Set, Union

from .base import Validator
from .errors import FieldValidationError


class ChoicesValidator(Validator):  # pylint: disable=too-few-public-methods
    """
    Validate user input against set of values.
    """
    _choices: Optional[Set[str]] = None

    def __init__(self, choices: Optional[Iterable[str]] = None) -> None:
        self._choices = set(choices) if choices else None
        super().__init__()

    async def validate(self, value) -> None:
        """
        Validate user input belongs to given list.

        :param value: User input
        """
        if value not in self._choices:
            raise FieldValidationError('Value should be one of the list!')


class RegexValidator(Validator):  # pylint: disable=too-few-public-methods
    """
    Validate user input with regular expression check.
    """

    def __init__(self, regex: str, error_message: str) -> None:
        self._error_message = error_message
        self._regex = re.compile(regex)

    async def validate(self, value) -> None:
        """
        Validate value matches regex.

        :param value: user input
        """
        if not bool(self._regex.match(value)):
            raise FieldValidationError(self._error_message)
