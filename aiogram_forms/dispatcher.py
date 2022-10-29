from typing import Type, MutableMapping

from aiogram import Dispatcher, Router, types
from aiogram.fsm.context import FSMContext

from .base import EntityContainer
from .states import EntityContainerStatesGroup


class EntityDispatcher:
    _registry: MutableMapping[str, Type['EntityContainer']] = {}

    _dp: Dispatcher
    _router: Router

    def __init__(self):
        self._router = Router()

    def attach(self, dp: Dispatcher):
        self._dp = dp
        dp.include_router(self._router)

    def register(self, name: str):
        def wrapper(container: Type[EntityContainer]):
            EntityContainerStatesGroup.bind(container)

            for filter_type, filter_ in container.filters().items():
                getattr(self._router, str(filter_type.value))(filter_)(container.handler)

            self._registry[name] = container
            return container
        return wrapper

    async def show(self, name: str, message: types.Message, state: FSMContext):
        entity = self._registry[name]

        # TODO: find a way to skip `message` and `state` passing
        await entity.show(message, state)


dispatcher = EntityDispatcher()
