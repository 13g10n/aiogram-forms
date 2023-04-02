from unittest.mock import AsyncMock, Mock, patch

import pytest

from aiogram_forms import dispatcher, FormsManager
from aiogram_forms.errors import ValidationError
from aiogram_forms.forms import Form, fields


@pytest.fixture
def event():
    return AsyncMock()


@pytest.fixture
def validation_error():
    return ValidationError(message='Failed!', code='error')


@pytest.fixture
def form(validation_error):
    def failing_validator(value: str):
        raise validation_error

    class TestForm(Form):
        test = fields.TextField('Test', validators=[failing_validator])

    dispatcher.register('test')(TestForm)
    return TestForm


@pytest.fixture
def dp(form, event):
    dp = Mock()
    dp.get_entity_container = Mock(return_value=form)
    return dp


@pytest.fixture
def manager(form, event, dp):
    state = AsyncMock()
    state.get_state = AsyncMock(return_value=form.state.__all_states_names__[0])

    return FormsManager(dp, event, data=dict(state=state))


@pytest.mark.asyncio
async def test_manager_show_not_subclass_form(manager, dp):
    with patch.object(dp, 'get_entity_container', return_value=object) as dp_mock:
        with pytest.raises(ValueError):
            await manager.show('unregistered')
        dp_mock.assert_called_once_with(Form, 'unregistered')


@pytest.mark.asyncio
async def test_manager_validation_raises(manager, form, validation_error):
    await manager.handle(form)
    manager.event.answer.assert_called_with(validation_error.message, reply_markup=form.test.reply_keyboard)


@pytest.mark.asyncio
async def test_get_data_by_form(manager, form):
    form_data = {'foo': '42'}
    manager.state.get_data = AsyncMock(return_value={form.__name__: form_data})
    assert await manager.get_data(form) == form_data


@pytest.mark.asyncio
async def test_get_data_by_form_deprecated(manager, form):
    manager.state.get_data = AsyncMock(return_value={form.__name__: {}})
    with pytest.deprecated_call():
        await manager.get_data(form)


@pytest.mark.asyncio
async def test_get_data_by_name(manager, form):
    form_data = {'foo': '42'}
    manager.state.get_data = AsyncMock(return_value={form.__name__: form_data})
    assert await manager.get_data('test') == form_data


@pytest.mark.asyncio
async def test_get_corrupted_data(manager, form):
    form_data = 'CORRUPTED'
    manager.state.get_data = AsyncMock(return_value={form.__name__: form_data})
    assert await manager.get_data('test') == {}
