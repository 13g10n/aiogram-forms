"""
Forms manager.
"""
import warnings
from typing import Type, cast, Optional, Dict, Any, Union

from aiogram.fsm.context import FSMContext

from .base import Field, Form
from ..errors import ValidationError
from ..core.manager import EntityManager
from ..core.states import EntityState


class FormsManager(EntityManager):
    """Forms manager."""
    state: FSMContext

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(*args, **kwargs)
        self.state = self.data['state']

    async def show(self, name: str) -> None:
        entity_container: Type['Form'] = self._get_form_by_name(name)

        first_entity = cast(Field, entity_container.state.get_states()[0].entity)
        await self.state.set_state(first_entity.state)
        await self.event.answer(first_entity.label, reply_markup=first_entity.reply_keyboard)  # type: ignore[arg-type]

    async def handle(self, form: Type['Form']) -> None:
        """Handle form field."""
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
            error_message = field.error_messages.get(error.code) or error.message
            await self.event.answer(error_message, reply_markup=field.reply_keyboard)  # type: ignore[arg-type]
            return

        data = await self.state.get_data()
        form_data = data.get(form.__name__, {})
        form_data.update({field.state.state.split(':')[-1]: value})  # type: ignore[union-attr]
        await self.state.update_data({form.__name__: form_data})

        next_state_index = cast(
            Dict['EntityState', Optional['EntityState']],
            dict(zip(current_state.group, list(current_state.group)[1:]))
        )
        next_entity_state: Optional['EntityState'] = next_state_index.get(current_state)
        if next_entity_state:
            next_field: Field = cast(Field, next_entity_state.entity)
            await self.state.set_state(next_field.state)
            await self.event.answer(
                '\n'.join([
                    str(next_field.label),
                    str(next_field.help_text) or ""
                ] if next_field.help_text else [str(next_field.label)]),
                reply_markup=next_field.reply_keyboard
            )
        else:
            await self.state.set_state(None)
            await form.callback(self.event, **self.data)

    async def get_data(self, form: Union[Type['Form'], str]) -> Dict[str, Any]:
        """Get form data from store."""
        container: Type['Form']
        if isinstance(form, str):
            container = self._get_form_by_name(form)
        else:
            warnings.warn(
                message='`FormsManager.get_data(...)` should accept form ID, '
                        'form class passing will be deprecated in next releases.',
                category=DeprecationWarning
            )
            container = form

        data = await self.state.get_data()
        form_data = data.get(container.__name__)
        if not form_data or not isinstance(form_data, dict):
            return {}
        return form_data

    def _get_form_by_name(self, name: str) -> Type['Form']:
        """Get registered form by name."""
        entity_container: Type['Form'] = cast(
            Type['Form'],
            self._dispatcher.get_entity_container(Form, name)
        )

        if not issubclass(entity_container, Form):
            raise ValueError(f'Entity registered with name {name} is not a valid form!')
        return entity_container
