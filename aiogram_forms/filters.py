"""
Aiogram events filters.
"""
import abc
from typing import TYPE_CHECKING, Type

from aiogram import types
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext

if TYPE_CHECKING:
    from aiogram_forms.core.states import EntityContainerStatesGroup


class EntityFilter(Filter, abc.ABC):
    """Basic entity filter."""

    def __init__(self, state: Type['EntityContainerStatesGroup']) -> None:
        self._state = state


class EntityStatesFilter(EntityFilter):
    """Filter by entity states."""

    async def __call__(self, message: types.Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        return current_state in [x.state for x in self._state]


class EntityDataFilter(EntityFilter):
    """Filter by entity callback data."""

    async def __call__(self, message: types.Message, state: FSMContext) -> bool:
        return message.data in [str(x.state) for x in self._state]
