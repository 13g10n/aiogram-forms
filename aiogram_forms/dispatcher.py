from typing import Type, MutableMapping

from aiogram import Dispatcher, Router

from .core.entities import EntityContainer
from .core.states import EntityContainerStatesGroup
from .middleware import EntityMiddleware


class EntityDispatcher:
    _registry: MutableMapping[str, Type['EntityContainer']] = {}

    _dp: Dispatcher
    _router: Router

    def __init__(self):
        self._router = Router()

    def attach(self, dp: Dispatcher):
        self._dp = dp

        # TODO: add other types of events
        self._dp.message.middleware(EntityMiddleware(self))

        dp.include_router(self._router)

    def register(self, name: str):
        def wrapper(container: Type[EntityContainer]):
            EntityContainerStatesGroup.bind(container)

            for filter_type, filter_ in container.filters().items():
                getattr(self._router, str(filter_type.value))(filter_)(container.handler)

            self._registry[name] = container
            return container
        return wrapper


dispatcher = EntityDispatcher()
