import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram_forms import FormsManager
    from aiogram_forms.menus.manager import MenusManager


class Action(abc.ABC):

    forms: 'FormsManager'
    menus: 'MenusManager'

    @abc.abstractmethod
    async def execute(self):
        pass


class NoAction(Action):

    async def execute(self):
        pass


class ShowForm(Action):

    def __init__(self, name: str):
        self.name = name

    async def execute(self):
        await self.forms.show(self.name)


class ShowMenu(Action):

    def __init__(self, name: str):
        self.name = name

    async def execute(self):
        await self.menus.show(self.name)
