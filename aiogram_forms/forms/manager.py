from typing import Type, cast

from . import Form
from .base import Field
from ..core.entities import EntityContainer
from ..core.manager import EntityManager


class FormsManager(EntityManager):

    async def show(self, name: str):
        fsm_state = self.data['state']
        entity_container: Type['EntityContainer'] = self._dispatcher.get_entity_container(Form, name)

        if not issubclass(entity_container, Form):
            raise ValueError(f'Entity registered with name {name} is not a valid form!')

        first_entity = cast(Field, entity_container.state.get_states()[0].entity)
        await fsm_state.set_state(first_entity.state)
        await self.event.answer(first_entity.label, reply_markup=first_entity.reply_keyboard)
