import abc
from typing import Dict, Any

from aiogram import types


class EntityManager(abc.ABC):

    def __init__(
            self,
            dispatcher,
            event: types.Message,
            data: Dict[str, Any]
    ) -> None:
        self.dispatcher = dispatcher
        self.event = event
        self.data = data

    @abc.abstractmethod
    async def show(self, name: str): pass
