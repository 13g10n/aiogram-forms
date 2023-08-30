"""
Forms manager.
"""
import warnings
from typing import Type, cast, Optional, Dict, Any, Union, TYPE_CHECKING

from aiogram.fsm.context import FSMContext

from .base import Field, Form
from ..errors import ValidationError
from ..core.manager import EntityManager
from ..core.states import EntityState

if TYPE_CHECKING:
    from ..manager import Manager


class FormsManager(EntityManager):
    """Forms manager."""
    state: FSMContext
    manager: 'Manager'

    def __init__(self, manager: 'Manager', *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.state = self.data['state']

    async def show(self, container: Type['Form']) -> None:
        first_entity = cast(Field, container.state.get_states()[0].entity)
        await self.state.set_state(first_entity.state)
        await self.message.answer(first_entity.label, reply_markup=first_entity.reply_keyboard)  # type: ignore[arg-type]

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
            await self.message.answer(error_message, reply_markup=field.reply_keyboard)  # type: ignore[arg-type]
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
            await self.message.answer(
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
            container = self.get_container_by_name(form)
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
