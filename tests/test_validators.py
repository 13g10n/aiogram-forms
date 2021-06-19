import pytest
from parameterized import parameterized

from aiogram_forms.validators import ChoicesValidator, EmailValidator


@parameterized.expand([
    ['Existing value', ['Minsk', 'Moscow', 'London'], 'Moscow'],
])
@pytest.mark.asyncio
async def test_choices_validator_existing_values_true(_, values, value):
    assert await ChoicesValidator(values).validate(value) is True


@parameterized.expand([
    ['Not existing value', ['Minsk', 'Moscow', 'London'], 'Boston'],
    ['Part of existing value', ['Minsk', 'Moscow', 'London'], 'cow'],
    ['Empty value', ['Minsk', 'Moscow', 'London'], ''],
])
@pytest.mark.asyncio
async def test_choices_validator_invalid_values_false(_, values, value):
    assert await ChoicesValidator(values).validate(value) is False


@parameterized.expand([
    ['Simple email', 'test@example.com'],
    ['Email with dot', 'test.name@example.com'],
    ['Email with subdomain', 'test@sub.example.com'],
])
@pytest.mark.asyncio
async def test_email_validator_valid_values_true(_, email):
    assert await EmailValidator().validate(email) is True


@parameterized.expand([
    ['Not email', 'test'],
    ['Simple domain', 'example.com'],
    ['Not valid email', '42@test@example.com'],
])
@pytest.mark.asyncio
async def test_email_validator_invalid_values_false(_, email):
    assert await EmailValidator().validate(email) is False
