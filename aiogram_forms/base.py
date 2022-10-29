import abc
from typing import TYPE_CHECKING, Optional, Type, Mapping

from aiogram.filters import Filter

from .enums import RouterHandlerType

if TYPE_CHECKING:
    from .states import EntityContainerStatesGroup, EntityState


class Entity:
    state: 'EntityState'
    label: str

    # TODO: move to forms only
    prev: Optional['Entity']
    next: Optional['Entity']


class EntityContainer(abc.ABC):
    state: Type['EntityContainerStatesGroup'] = None

    @classmethod
    @abc.abstractmethod
    def filters(cls, *args, **kwargs) -> Mapping[RouterHandlerType, Filter]:
        """Event filters."""

    @classmethod
    @abc.abstractmethod
    async def handler(cls, *args, **kwargs) -> None:
        """Event handler."""

    @classmethod
    @abc.abstractmethod
    async def show(cls, *args, **kwargs) -> None:
        """Start."""
