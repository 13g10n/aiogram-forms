"""
Code entity manager.
"""
import abc
from typing import TYPE_CHECKING, Dict, Any, Type

from aiogram import types


if TYPE_CHECKING:
    from .entities import EntityContainer
    from .. import EntityDispatcher  # type: ignore[attr-defined]


class EntityManager(abc.ABC):  # pylint: disable=too-few-public-methods
    """Entity manager."""

    def __init__(
            self,
            dispatcher: 'EntityDispatcher',
            event: types.Message,
            data: Dict[str, Any]
    ) -> None:
        self._dispatcher = dispatcher
        self.event = event
        self.data = data

    @abc.abstractmethod
    async def show(self, container: Type['EntityContainer']) -> None:
        """Start entity propagation."""

    @abc.abstractmethod
    async def handle(self, container: Type['EntityContainer']) -> None:
        """Handle entity callback."""

    def get_container_by_name(self, name: str) -> Type['EntityContainer']:
        return self._dispatcher.get_entity_container(name)

    @property
    def message(self) -> types.Message:
        return self.event.message if isinstance(self.event, types.CallbackQuery) else self.event
