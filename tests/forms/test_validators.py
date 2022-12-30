from contextlib import nullcontext

import pytest

from aiogram_forms.errors import ValidationError
from aiogram_forms.forms import validators


@pytest.mark.parametrize(
    'limit,value,exception',
    [
        (-3, 'foo', nullcontext()),
        (3, '12', pytest.raises(ValidationError)),
        (3, '123', nullcontext()),
        (3, '1234', nullcontext()),
    ],
    ids=[
        'Passes when negative number',
        'Fails when less characters',
        'Passes when same length',
        'Passes when greater length'
    ]
)
def test_min_length_validator(limit: int, value: str, exception: bool):
    with exception:
        validators.MinLengthValidator(limit)(value)


@pytest.mark.parametrize(
    'limit,value,exception',
    [
        (-3, 'foo', pytest.raises(ValidationError)),
        (3, '1234', pytest.raises(ValidationError)),
        (3, '123', nullcontext()),
        (3, '12', nullcontext()),
    ],
    ids=[
        'Fails when negative number',
        'Fails when greater characters',
        'Passes when same length',
        'Passes when less length'
    ]
)
def test_max_length_validator(limit: int, value: str, exception):
    with exception:
        validators.MaxLengthValidator(limit)(value)


@pytest.mark.parametrize(
    'regex,value,exception',
    [
        (r'a{3}$', 'bbb', pytest.raises(ValidationError)),
        (r'a{3}$', 'aaa', nullcontext()),
    ],
    ids=[
        'Fails when not contains',
        'Passes when contains'
    ]
)
def test_regex_validator(regex: str, value: str, exception):
    with exception:
        validators.RegexValidator(regex)(value)


@pytest.mark.parametrize(
    'value,exception',
    [
        ('test.email@example.com', nullcontext()),
        ('test.email@example', pytest.raises(ValidationError)),
        ('test.email', pytest.raises(ValidationError)),
    ],
    ids=[
        'Passes when valid email',
        'Fails when invalid domain',
        'Fails when contains no "@" sign'
    ]
)
def test_email_validator(value: str, exception):
    with exception:
        validators.EmailValidator()(value)


@pytest.mark.parametrize(
    'value,exception',
    [
        ('+123456789012', nullcontext()),
        ('123456789012', nullcontext()),
        ('not even a number', pytest.raises(ValidationError))
    ],
    ids=[
        'Passes when valid phone',
        'Passes when valid phone without "+" sign',
        'Fails when invalid format'
    ]
)
def test_phone_validator(value: str, exception):
    with exception:
        validators.PhoneNumberValidator()(value)
