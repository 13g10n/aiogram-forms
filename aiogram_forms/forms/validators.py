# pylint: disable=too-few-public-methods
"""
Form fields validators.
"""
import re
from typing import Tuple, Any

from aiogram_forms.errors import ValidationError


class MinLengthValidator:
    """Min length validator."""

    def __init__(self, limit: int) -> None:
        self.limit = limit

    def __call__(self, value: str) -> None:
        if len(value) < self.limit:
            raise ValidationError(f'Value should be at least {self.limit} characters.', code='min_length')


class MaxLengthValidator:
    """Max length validator."""

    def __init__(self, limit: int) -> None:
        self.limit = limit

    def __call__(self, value: str) -> None:
        if len(value) > self.limit:
            raise ValidationError(f'Value should be at most {self.limit} characters.', code='max_length')


class RegexValidator:
    """Regex validator."""
    error: ValidationError = ValidationError('Value if in invalid format.', code='regex')

    def __init__(self, regex: str) -> None:
        self.regex = re.compile(regex)

    def __call__(self, value: str) -> None:
        match = self.regex.match(value)
        if not match:
            raise self.error


class EmailValidator(RegexValidator):
    """Email validator.

    Exactly one "@" sign and at least one "." in the part after the @.
    """
    error = ValidationError('Value should be valid email address.', code='email')

    def __init__(self, regex: str = r'[^@]+@[^@]+\.[^@]+') -> None:
        super().__init__(regex)


class PhoneNumberValidator(RegexValidator):
    """Phone number validator.

    Reference: https://ihateregex.io/expr/phone/
    """
    error = ValidationError('Value should be a valid phone number.', code='phone')

    def __init__(self, regex: str = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'):
        super().__init__(regex)


class ChoiceValidator:
    """Choices validator.

    Validates only on given values.
    """
    error = ValidationError('Value is not allowed.', code='invalid_choice')

    def __init__(self, choices: Tuple[Any, ...]):
        self.choices = choices

    def __call__(self, value: str) -> None:
        if value not in self.choices:
            raise self.error
