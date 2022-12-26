from typing import TYPE_CHECKING, Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types

from .const import FORMS_MANAGER_DI_KEY
from .forms.manager import FormsManager

if TYPE_CHECKING:
    from aiogram_forms.dispatcher import EntityDispatcher


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
        data[FORMS_MANAGER_DI_KEY] = FormsManager(self.dispatcher, event, data)
        return await handler(event, data)