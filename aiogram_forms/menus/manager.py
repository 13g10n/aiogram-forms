"""
Menus manager.
"""
from typing import Type, cast

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from . import Menu, MenuItem
from .. import utils, FormsManager
from ..core.manager import EntityManager


class MenusManager(EntityManager):
    """Menus manager."""
    event: types.CallbackQuery

    _args: tuple
    _kwargs: dict

    def __init__(self, dispatcher, event: types.Message, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(dispatcher, event, *args, **kwargs)

        self.event = event

        # TODO: rework, event can be any type message or callback query
        if isinstance(event, types.CallbackQuery):
            self._args = (dispatcher, self.event.message, *args)
        else:
            self._args = (dispatcher, event, *args)

        self._kwargs = kwargs

    async def show(self, name: str) -> None:
        menu: Type[Menu] = self._get_menu_by_name(name)

        builder = InlineKeyboardBuilder()

        for _, menu_item in utils.get_attrs_of_type(menu, MenuItem):
            builder.row(InlineKeyboardButton(
                text=menu_item.label,
                callback_data=str(menu_item.state.state)
            ))

        # TODO: custom message (menu title?)
        await self.event.answer('Menu', reply_markup=builder.as_markup())

    async def handle(self, menu: Type[Menu]) -> None:
        """Handle menu button."""
        item = None

        for _, menu_item in utils.get_attrs_of_type(menu, MenuItem):
            if menu_item.state.state == self.event.data:
                item = menu_item
                print(f'>> {menu_item.label}')

        item.action.menus = MenusManager(*self._args, **self._kwargs)
        item.action.forms = FormsManager(*self._args, **self._kwargs)

        await self.event.answer()
        await item.action.execute()

    def _get_menu_by_name(self, name: str) -> Type[Menu]:
        entity_container = cast(
            Type[Menu],
            self._dispatcher.get_entity_container(Menu, name)
        )

        if not issubclass(entity_container, Menu):
            raise ValueError(f'Entity registered with name {name} is not a valid menu!')
        return entity_container
