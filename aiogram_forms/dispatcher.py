"""
Entity dispatcher.
"""
from collections import defaultdict
from typing import Type, MutableMapping, Dict, Any, Callable, Awaitable

from aiogram import Dispatcher, Router, types

from .core.entities import EntityContainer
from .core.states import EntityContainerStatesGroup
from .manager import Manager
from .middleware import EntityMiddleware


class EntityDispatcher:
    """Entity dispatcher."""
    _registry: MutableMapping[
        str,
        MutableMapping[str, Type['EntityContainer']]
    ] = {}

    _dp: Dispatcher
    _router: Router

    def __init__(self) -> None:
        self._router = Router()

    def attach(self, dp: Dispatcher) -> None:  # pylint: disable=invalid-name
        """Attach aiogram dispatcher."""
        self._dp = dp
        self._dp.message.middleware(EntityMiddleware(self))

        dp.include_router(self._router)

    def register(self, name: str) -> Callable[[Type[EntityContainer]], Type[EntityContainer]]:
        """Register entity with given name."""
        def wrapper(container: Type[EntityContainer]) -> Type[EntityContainer]:
            EntityContainerStatesGroup.bind(container)

            for filter_type, filter_ in container.filters().items():
                getattr(self._router, str(filter_type.value))(filter_)(self._get_entity_container_handler(container))

            self._registry[name] = container
            return container
        return wrapper

    def get_entity_container(self, name: str) -> Type[EntityContainer]:
        """Het entity container by name and type."""
        entity_container = self._registry.get(name)
        if entity_container:
            return entity_container
        raise ValueError(f'There are no entity container with name "{name}"!')

    def _get_entity_container_handler(
            self, container: Type['EntityContainer']
    ) -> Callable[..., Awaitable[None]]:
        """Get entity container event handler."""
        async def message_handler(event: types.Message, **data: Dict[str, Any]) -> None:
            """Entity container event handler, redirect to manager."""
            await Manager(self, event, data).handle(container)

        return message_handler
