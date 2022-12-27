from typing import Type, cast, Optional

from aiogram.fsm.context import FSMContext

from . import Form
from .base import Field
from .errors import ValidationError
from ..core.entities import EntityContainer
from ..core.manager import EntityManager
from ..core.states import EntityState


class FormsManager(EntityManager):
    state: FSMContext

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = self.data['state']

    async def show(self, name: str):
        entity_container: Type['EntityContainer'] = self._dispatcher.get_entity_container(Form, name)

        if not issubclass(entity_container, Form):
            raise ValueError(f'Entity registered with name {name} is not a valid form!')

        first_entity = cast(Field, entity_container.state.get_states()[0].entity)
        await self.state.set_state(first_entity.state)
        await self.event.answer(first_entity.label, reply_markup=first_entity.reply_keyboard)

    async def handle(self, form: Type['Form']) -> None:
        state_label = await self.state.get_state()
        current_state: 'EntityState' = next(iter([
            st for st in form.state.get_states() if st.state == state_label
        ]))

        field: Field = cast(Field, current_state.entity)
        try:
            value = await field.process(
                await field.extract(self.event)
            )
            await field.validate(value)
        except ValidationError as error:
            await self.event.answer(error.message, reply_markup=field.reply_keyboard)
            return

        # TODO: save to state

        next_state_index = dict(zip(current_state.group, list(current_state.group)[1:]))
        next_entity_state: Optional['EntityState'] = next_state_index.get(current_state)
        if next_entity_state:
            next_field: Field = cast(Field, next_entity_state.entity)
            await self.state.set_state(next_field.state)
            await self.event.answer(next_field.label, reply_markup=next_field.reply_keyboard)
        else:
            await self.state.set_state(None)
            # TODO: add callbacks
            # await cls.callback(message, state, *args, **kwargs)
