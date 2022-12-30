from unittest.mock import AsyncMock, patch, Mock

import pytest

from aiogram_forms import dispatcher
from aiogram_forms.forms import Form, FormsManager, fields


class ExampleForm(Form):
    first = fields.TextField('First')
    second = fields.TextField('Second')


@pytest.mark.asyncio
async def test_flow():
    """Test whole form flow."""

    with patch.object(dispatcher, '_router', Mock(message=Mock())) as router_mock:
        dispatcher.register('example')(ExampleForm)

    handler = router_mock.message.return_value.call_args.args[0]
    fsm = AsyncMock()

    message = AsyncMock(text='Start form.')
    manager = FormsManager(dispatcher, message, data=dict(state=fsm))
    await manager.show('example')

    fsm.set_state.assert_called_once_with(ExampleForm.first.state.state)
    message.answer.assert_called_once_with('First', reply_markup=ExampleForm.first.reply_keyboard)

    fsm.get_state = AsyncMock(return_value=ExampleForm.first.state.state)
    fsm.get_data = AsyncMock(return_value={})
    message = AsyncMock(text='First value')
    await handler(message, state=fsm)

    fsm.set_state.assert_called_with(ExampleForm.second.state.state)
    fsm.update_data.assert_called_once_with({'ExampleForm': {'first': 'First value'}})
    message.answer.assert_called_once_with('Second', reply_markup=ExampleForm.first.reply_keyboard)

    fsm = AsyncMock()
    fsm.get_state = AsyncMock(return_value=ExampleForm.second.state.state)
    fsm.get_data = AsyncMock(return_value={'ExampleForm': {'first': 'First value'}})
    message = AsyncMock(text='Second value')
    ExampleForm.callback = AsyncMock()
    await handler(message, state=fsm)

    fsm.set_state.assert_called_with(None)
    fsm.update_data.assert_called_once_with({'ExampleForm': {'first': 'First value', 'second': 'Second value'}})
    ExampleForm.callback.assert_called_once()
