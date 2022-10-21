import pytest
from parameterized import parameterized

from aiogram_forms.errors import FieldValidationError
from aiogram_forms.validators import ChoicesValidator


@parameterized.expand([
    ['Existing value', ['Minsk', 'Moscow', 'London'], 'Moscow'],
])
@pytest.mark.asyncio
async def test_choices_validator_existing_values(_, values, value):
    await ChoicesValidator(values).validate(value)


@parameterized.expand([
    ['Not existing value', ['Minsk', 'Moscow', 'London'], 'Boston'],
    ['Part of existing value', ['Minsk', 'Moscow', 'London'], 'cow'],
    ['Empty value', ['Minsk', 'Moscow', 'London'], ''],
])
@pytest.mark.asyncio
async def test_choices_validator_invalid_values_raises(_, values, value):
    with pytest.raises(FieldValidationError):
        await ChoicesValidator(values).validate(value)
