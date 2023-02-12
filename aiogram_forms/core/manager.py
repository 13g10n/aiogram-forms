"""
Code entity manager.
"""
import abc
from typing import TYPE_CHECKING, Dict, Any

from aiogram import types

if TYPE_CHECKING:
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
    async def show(self, name: str) -> None:
        """Start entity propagation."""
