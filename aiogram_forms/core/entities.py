import abc
from typing import TYPE_CHECKING, Type, Mapping

if TYPE_CHECKING:
    from aiogram.filters import Filter

    from .states import EntityContainerStatesGroup, EntityState
    from ..enums import RouterHandlerType


class Entity:
    """Base class for containing item."""
    state: 'EntityState'
    label: str


class EntityContainer(abc.ABC):
    """Base class for Entity container implementation."""
    state: Type['EntityContainerStatesGroup'] = None

    @classmethod
    @abc.abstractmethod
    def filters(cls, *args, **kwargs) -> Mapping['RouterHandlerType', 'Filter']:
        """Event filters."""
