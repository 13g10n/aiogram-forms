from typing import TYPE_CHECKING, Type

from aiogram import types
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext

if TYPE_CHECKING:
    from aiogram_forms.core.states import EntityContainerStatesGroup


class EntityStatesFilter(Filter):
    def __init__(self, state: Type['EntityContainerStatesGroup']) -> None:
        self._state = state

    async def __call__(self, message: types.Message, state: FSMContext) -> bool:
        state = await state.get_state()
        return state in [x.state for x in self._state]


class EntityCallbackFilter(Filter):
    def __init__(self, state: Type['EntityContainerStatesGroup']) -> None:
        self._state = state

    async def __call__(self, *args, **kwargs) -> bool:
        return kwargs['event_update'].callback_query.data in [s.state for s in self._state.get_states()]
