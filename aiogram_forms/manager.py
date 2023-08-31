from typing import Type, Callable

from aiogram_forms import Form, FormsManager
from aiogram_forms.core.entities import EntityContainer
from aiogram_forms.core.manager import EntityManager
from aiogram_forms.menus import Menu
from aiogram_forms.menus.manager import MenusManager


class Manager(EntityManager):
    """Supreme entity manager."""
    forms: FormsManager
    menus: MenusManager

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.forms = FormsManager(self, *args, **kwargs)
        self.menus = MenusManager(self, *args, **kwargs)

    async def show(self, name: str, **options) -> None:
        container: Type['EntityContainer'] = self.get_container_by_name(name)
        await self._call_entity_manager_method(container, EntityManager.show, **options)

    async def handle(self, container: Type[EntityContainer]) -> None:
        await self._call_entity_manager_method(container, EntityManager.handle)

    async def _call_entity_manager_method(self, container: Type[EntityContainer], method: Callable, **options):
        if not issubclass(container, (Form, Menu)):
            raise RuntimeError(f'Container of type "{container.__class__.__name__}" is not supported!')

        container_manager = self.forms if issubclass(container, Form) else self.menus
        await getattr(container_manager, method.__name__)(container, **options)
