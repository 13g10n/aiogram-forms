from collections import namedtuple
from unittest.mock import AsyncMock

import pytest

from aiogram_forms.forms.fields import Field

TEST_LABEL = 'Test Label'


@pytest.fixture
def event():
    FakeEvent = namedtuple('FakeMessage', ['text'])
    return FakeEvent('42')


@pytest.fixture
def field():
    return Field(TEST_LABEL)


def test_label_set(field) -> None:
    assert field.label == TEST_LABEL


@pytest.mark.asyncio
async def test_extract_returns_event_text(field, event) -> None:
    assert await field.extract(event) == event.text


@pytest.mark.asyncio
async def test_process_returns_untouched_value(field, event) -> None:
    assert await field.process(event.text) == event.text


@pytest.mark.asyncio
async def test_validate_calls_single_validator(event) -> None:
    validator_mock = AsyncMock()
    field = Field(TEST_LABEL, validators=[validator_mock])
    assert await field.validate(event.text) is None
    validator_mock.assert_called_once_with(event.text)


@pytest.mark.asyncio
async def test_validate_calls_multiple_validators(event) -> None:
    validator_mocks = [AsyncMock() for _ in range(5)]
    field = Field(TEST_LABEL, validators=validator_mocks)
    assert await field.validate(event.text) is None
    for mock in validator_mocks:
        mock.assert_called_once_with(event.text)
