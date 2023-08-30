"""
Dependency injector.
"""
from typing import TYPE_CHECKING, Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types

from .manager import Manager
from .const import MANAGER_DI_KEY

if TYPE_CHECKING:
    from aiogram_forms.dispatcher import EntityDispatcher


class EntityMiddleware(BaseMiddleware):  # pylint: disable=too-few-public-methods
    """Entity middleware."""
    dispatcher: 'EntityDispatcher'

    def __init__(self, dispatcher: 'EntityDispatcher') -> None:
        self.dispatcher = dispatcher

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data[MANAGER_DI_KEY] = Manager(self.dispatcher, event, data)
        return await handler(event, data)
