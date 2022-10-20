import pytest
from parameterized import parameterized

from aiogram_forms.validators import ChoicesValidator


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
