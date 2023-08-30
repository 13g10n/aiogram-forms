from unittest.mock import Mock, AsyncMock

import pytest

from aiogram.fsm.state import State

from aiogram_forms.core.states import EntityContainerStatesGroup
from aiogram_forms.filters import EntityStatesFilter


@pytest.fixture
def state_group():
    class ExampleStatesGroup(EntityContainerStatesGroup):
        first = State()
        second = State()
        third = State()
    return ExampleStatesGroup


@pytest.fixture
def entity_states_filter(state_group):
    return EntityStatesFilter(state_group)


# @pytest.fixture
# def entity_callback_filter(state_group):
#     return EntityCallbackFilter(state_group)


@pytest.mark.asyncio
async def test_entity_states_filter_valid_state(entity_states_filter, state_group):
    fsm_context = Mock()
    fsm_context.get_state = AsyncMock(return_value=state_group.first)
    assert await entity_states_filter(None, fsm_context)  # noqa
    fsm_context.get_state.assert_called_once()


@pytest.mark.asyncio
async def test_entity_states_filter_invalid_state(entity_states_filter):
    fsm_context = Mock()
    fsm_context.get_state = AsyncMock(return_value=42)
    assert not await entity_states_filter(None, fsm_context)  # noqa


# @pytest.mark.asyncio
# async def test_callback_data_filter_valid_data(entity_callback_filter, state_group):
#     event_update = Mock()
#     event_update.callback_query = Mock()
#     event_update.callback_query.data = state_group.first
#
#     assert await entity_callback_filter(event_update=event_update)  # noqa
#
#
# @pytest.mark.asyncio
# async def test_callback_data_filter_invalid_data(entity_callback_filter):
#     event_update = Mock()
#     event_update.callback_query = Mock()
#     event_update.callback_query.data = '42'
#
#     assert not await entity_callback_filter(event_update=event_update)  # noqa
