"""
Core entity types.
"""
import abc
from typing import TYPE_CHECKING, Type, Mapping

if TYPE_CHECKING:
    from aiogram.filters import Filter

    from .states import EntityContainerStatesGroup, EntityState
    from ..enums import RouterHandlerType
    from ..types import TranslatableString


class Entity:  # pylint: disable=too-few-public-methods
    """Base class for containing item."""
    state: 'EntityState'
    label: 'TranslatableString'


class EntityContainer(abc.ABC):  # pylint: disable=too-few-public-methods
    """Base class for Entity container implementation."""
    state: Type['EntityContainerStatesGroup'] = None

    @classmethod
    @abc.abstractmethod
    def filters(cls, *args, **kwargs) -> Mapping['RouterHandlerType', 'Filter']:
        """Event filters."""
