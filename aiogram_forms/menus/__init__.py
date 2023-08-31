from typing import Tuple, Any, Dict, Mapping, Optional

from aiogram.filters import Filter

from aiogram_forms.core.entities import Entity, EntityContainer
from aiogram_forms.enums import RouterHandlerType
from aiogram_forms.filters import EntityDataFilter
from aiogram_forms.menus.actions import Action, NoAction


class MenuItem(Entity):

    def __init__(self, label: str, action: Optional[Action] = None) -> None:
        self.label = label
        self.action = action or NoAction()


class Menu(EntityContainer):

    @classmethod
    def filters(cls, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Mapping[RouterHandlerType, Filter]:
        """Form handler filters."""
        return {
            RouterHandlerType.CallbackQuery: EntityDataFilter(cls.state)
        }

    @classmethod
    async def title(cls) -> str:
        """Menu title message customisation."""
        return 'Menu'
