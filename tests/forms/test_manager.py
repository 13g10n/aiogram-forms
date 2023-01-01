from unittest.mock import AsyncMock, Mock

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
def manager(form, event):
    dispatcher = Mock()
    dispatcher.get_entity_container = Mock(return_value=object)

    state = AsyncMock()
    state.get_state = AsyncMock(return_value=form.state.__all_states_names__[0])

    return FormsManager(dispatcher, event, data=dict(state=state))


@pytest.mark.asyncio
async def test_manager_show_not_subclass_form(manager):
    with pytest.raises(ValueError):
        await manager.show('unregistered')


@pytest.mark.asyncio
async def test_manager_validation_raises(manager, form, validation_error):
    await manager.handle(form)
    manager.event.answer.assert_called_with(validation_error.message, reply_markup=form.test.reply_keyboard)


@pytest.mark.asyncio
async def test_get_data(manager, form):
    form_data = {'foo': '42'}
    manager.state.get_data = AsyncMock(return_value={form.__name__: form_data})
    assert await manager.get_data(form) == form_data
