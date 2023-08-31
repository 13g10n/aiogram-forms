"""
Menus manager.
"""
from typing import Type, TYPE_CHECKING

from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from . import Menu, MenuItem
from .. import utils
from ..core.manager import EntityManager

if TYPE_CHECKING:
    from ..manager import Manager


class MenusManager(EntityManager):
    """Menus manager."""
    manager: 'Manager'

    def __init__(self, manager: 'Manager', dispatcher, event: types.Message, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(dispatcher, event, *args, **kwargs)
        self.manager = manager

    async def show(self, menu: Type[Menu], replace: bool = False) -> None:
        builder = InlineKeyboardBuilder()

        for _, menu_item in utils.get_attrs_of_type(menu, MenuItem):
            builder.row(InlineKeyboardButton(
                text=menu_item.label,
                callback_data=str(menu_item.state.state)
            ))

        if not replace:
            await self.message.answer(await menu.title(), reply_markup=builder.as_markup())
        else:
            await self.message.edit_text(await menu.title())
            await self.message.edit_reply_markup(reply_markup=builder.as_markup())

    async def handle(self, menu: Type[Menu]) -> None:
        """Handle menu button."""
        item = next(iter(
            menu_item for _, menu_item
            in utils.get_attrs_of_type(menu, MenuItem)
            if menu_item.state.state == self.event.data
        ))

        await self.event.answer(text='...', reply_markup=ReplyKeyboardRemove())
        await item.action.execute(self.manager)
