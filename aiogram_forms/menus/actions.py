import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram_forms import Manager


class Action(abc.ABC):

    @abc.abstractmethod
    async def execute(self, manager: 'Manager') -> None:
        pass


class NoAction(Action):

    async def execute(self, manager: 'Manager') -> None:
        pass


class ShowForm(Action):

    def __init__(self, name: str):
        self.name = name

    async def execute(self, manager: 'Manager') -> None:
        await manager.show(self.name)


class ShowMenu(Action):

    def __init__(self, name: str):
        self.name = name

    async def execute(self, manager: 'Manager') -> None:
        await manager.show(self.name, replace=True)


class Custom(Action):

    def __init__(self, callable):
        self.callable = callable

    async def execute(self, manager: 'Manager') -> None:
        await self.callable(manager)
