from typing import TYPE_CHECKING, Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types

from .forms.manager import FormsManager

if TYPE_CHECKING:
    from .dispatcher import EntityDispatcher


class EntityMiddleware(BaseMiddleware):
    dispatcher: 'EntityDispatcher'

    def __init__(self, dispatcher: 'EntityDispatcher') -> None:
        self.dispatcher = dispatcher

    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any]
    ) -> Any:
        data['forms'] = FormsManager(self.dispatcher, event, data)
        return await handler(event, data)
