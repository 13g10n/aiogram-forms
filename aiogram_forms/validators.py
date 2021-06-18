"""
User input validators
"""
import re
from typing import Optional, Iterable, Set

from .base import BaseValidator
from .const import EMAIL_REGEXP


class ChoicesValidator(BaseValidator):  # pylint: disable=too-few-public-methods
    """
    Validate user input against set of values
    """
    _choices: Optional[Set[str]] = None

    def __init__(self, choices: Optional[Iterable[str]] = None) -> None:
        self._choices = set(choices) if choices else None
        super().__init__()

    async def validate(self, value) -> bool:
        """
        Validate user input belongs to given list
        :param value: user input
        :return: bool
        """
        return value in self._choices


class RegexValidator(BaseValidator):  # pylint: disable=too-few-public-methods
    """
    Validate user input with regular expression check
    """

    def __init__(self, regex: str) -> None:
        self._regex = re.compile(regex)

    async def validate(self, value) -> bool:
        """
        Validate value matches regex
        :param value: user input
        :return: bool
        """
        return bool(self._regex.match(value))


class EmailValidator(RegexValidator):  # pylint: disable=too-few-public-methods
    """
    Validate user input is valid email address
    """

    def __init__(self):
        super().__init__(EMAIL_REGEXP)
