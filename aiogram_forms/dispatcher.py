from typing import Type, MutableMapping

from aiogram import Dispatcher, Router

from .core.entities import EntityContainer
from .core.states import EntityContainerStatesGroup
from .middleware import EntityMiddleware


class EntityDispatcher:
    _registry: MutableMapping[
        str,
        MutableMapping[str, Type['EntityContainer']]
    ] = {}

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

            if container.__name__ not in self._registry:
                # TODO: extend with menus
                self._registry['forms'] = {}

            self._registry['forms'][name] = container
            return container
        return wrapper

    def get_entity_container(self, container_type: Type[EntityContainer], name: str):
        entity_container = self._registry['forms'].get(name)
        if entity_container:
            return entity_container
        raise ValueError(f'There are no entity container with name "{name}" of type "{container_type.__name__}"!')
