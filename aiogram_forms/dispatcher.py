"""
Entity dispatcher.
"""
from typing import Type, MutableMapping, Callable, Any, TYPE_CHECKING

from aiogram import Dispatcher, Router
from aiogram.handlers import CallbackQueryHandler

from .core.entities import EntityContainer
from .core.states import EntityContainerStatesGroup
from .middleware import EntityMiddleware

if TYPE_CHECKING:
    from aiogram_forms import Manager


router = Router()


class EventHandler(CallbackQueryHandler):
    manager: 'Manager'
    container: Type[EntityContainer]

    def __init__(self, *args, manager: 'Manager', **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager

    async def handle(self) -> Any:
        await self.manager.handle(self.container)

    @classmethod
    def for_container(cls, container: Type[EntityContainer]):
        return type(f'Bound{cls.__name__}', (cls, ), {'container': container})


class EntityDispatcher:
    """Entity dispatcher."""
    _registry: MutableMapping[
        str,
        MutableMapping[str, Type['EntityContainer']]
    ] = {}

    _dp: Dispatcher

    def attach(self, dp: Dispatcher) -> None:  # pylint: disable=invalid-name
        """Attach aiogram dispatcher."""
        self._dp = dp

        # TODO: handle all types of events
        self._dp.message.middleware(EntityMiddleware(self))
        self._dp.callback_query.middleware(EntityMiddleware(self))

        dp.include_router(router)

    def register(self, name: str) -> Callable[[Type[EntityContainer]], Type[EntityContainer]]:
        """Register entity with given name."""
        def wrapper(container: Type[EntityContainer]) -> Type[EntityContainer]:
            EntityContainerStatesGroup.bind(container)

            for filter_type, filter_ in container.filters().items():
                getattr(router, str(filter_type.value))(filter_)(EventHandler.for_container(container))

            self._registry[name] = container
            return container
        return wrapper

    def get_entity_container(self, name: str) -> Type[EntityContainer]:
        """Het entity container by name and type."""
        entity_container = self._registry.get(name)
        if entity_container:
            return entity_container
        raise ValueError(f'There are no entity container with name "{name}"!')
