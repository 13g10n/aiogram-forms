"""
Aiogram events filters.
"""
from typing import TYPE_CHECKING, Type, Dict, Any, List

from aiogram import types
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext

if TYPE_CHECKING:
    from aiogram_forms.core.states import EntityContainerStatesGroup


class EntityStatesFilter(Filter):
    """Filter by entity states."""
    def __init__(self, state: Type['EntityContainerStatesGroup']) -> None:
        self._state = state

    async def __call__(self, message: types.Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        return current_state in [x.state for x in self._state]


class EntityCallbackFilter(Filter):
    """Filter by callback data."""
    def __init__(self, state: Type['EntityContainerStatesGroup']) -> None:
        self._state = state

    async def __call__(self, *args: List[Any], **kwargs: Dict[str, Any]) -> bool:
        callback_query_data = kwargs['event_update'].callback_query.data  # type: ignore[attr-defined]
        return callback_query_data in [s.state for s in self._state.get_states()]
