from unittest.mock import AsyncMock

import pytest

from aiogram_forms.forms.fields import Field

TEST_LABEL = 'Test Label'


@pytest.fixture
def field():
    return Field(TEST_LABEL)


def test_label_set(field) -> None:
    assert field.label == TEST_LABEL


@pytest.mark.asyncio
async def test_extract_returns_event_text(field, message) -> None:
    assert await field.extract(message) == message.text


@pytest.mark.asyncio
async def test_process_returns_untouched_value(field, message) -> None:
    assert await field.process(message.text) == message.text


@pytest.mark.asyncio
async def test_validate_calls_single_validator(message) -> None:
    validator_mock = AsyncMock()
    field = Field(TEST_LABEL, validators=[validator_mock])
    assert await field.validate(message.text) is None
    validator_mock.assert_called_once_with(message.text)


@pytest.mark.asyncio
async def test_validate_calls_multiple_validators(message) -> None:
    validator_mocks = [AsyncMock() for _ in range(5)]
    field = Field(TEST_LABEL, validators=validator_mocks)
    assert await field.validate(message.text) is None
    for mock in validator_mocks:
        mock.assert_called_once_with(message.text)
