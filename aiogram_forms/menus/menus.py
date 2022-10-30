from typing import Optional, Mapping

from aiogram.filters import Filter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..core.entities import Entity, EntityContainer
from ..enums import RouterHandlerType
from ..filters import EntityCallbackFilter


class MenuItem(Entity):
    _action: Optional[str]

    def __init__(
            self,
            label: str,
            action: Optional[str] = None
    ) -> None:
        self.label = label
        self._action = action


class Menu(EntityContainer):

    @classmethod
    def filters(cls, *args, **kwargs) -> Mapping[RouterHandlerType, Filter]:
        return {
            RouterHandlerType.CallbackQuery: EntityCallbackFilter(cls.state)
        }

    @classmethod
    async def handler(cls, *args, **kwargs) -> None:
        print(args)
        print(kwargs)
        # kwargs['event_update'].callback_query
        await kwargs['event_update'].callback_query.answer()

    @classmethod
    async def show(cls, message, state, *args, **kwargs) -> None:
        await message.answer(
            'Menu',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=state_.entity.label,
                            callback_data=state_.state
                        )
                    ] for state_ in cls.state.get_states()
                ]
            )
        )
