from typing import TYPE_CHECKING, Mapping, cast, List, Optional

from aiogram import types
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext

from .errors import ValidationError
from .validators import Validator
from ..core.entities import Entity, EntityContainer
from ..enums import RouterHandlerType
from ..filters import EntityStatesFilter

if TYPE_CHECKING:
    from aiogram_forms.core.states import EntityState


class Field(Entity):
    help_text: Optional[str] = None
    error_messages: Optional[Mapping[str, str]] = None
    validators: List[Validator]

    def __init__(
            self,
            label: str,
            help_text: Optional[str] = None,
            error_messages: Optional[Mapping[str, str]] = None,
            validators: Optional[List[Validator]] = None
    ) -> None:
        self.label = label
        self.help_text = help_text
        self.error_messages = error_messages
        self.validators = validators or []

    @property
    def reply_keyboard(self):
        return types.ReplyKeyboardRemove()

    async def validate(self, value: str) -> None:
        for validator in self.validators:
            await validator.validate(value)


class Form(EntityContainer):

    @classmethod
    def filters(cls, *args, **kwargs) -> Mapping[RouterHandlerType, Filter]:
        return {
            RouterHandlerType.Message: EntityStatesFilter(cls.state)
        }

    @classmethod
    async def handler(cls, message: types.Message, state: FSMContext, *args, **kwargs) -> None:
        state_label = await state.get_state()
        current_state: 'EntityState' = next(iter([
            st for st in cls.state.get_states() if st.state == state_label
        ]))

        field: Field = cast(Field, current_state.entity)
        try:
            # TODO: move data extraction to field (for custom processing)?
            if message.content_type == 'contact':
                await field.validate(message.contact.phone_number)
            else:
                await field.validate(message.text)
        except ValidationError as error:
            await message.answer(error.message, reply_markup=field.reply_keyboard)
            return

        # TODO: save to state

        next_entity: Field = cast(Field, current_state.entity.next)
        if next_entity:
            await state.set_state(next_entity.state)
            await message.answer(next_entity.label, reply_markup=next_entity.reply_keyboard)
        else:
            await state.set_state(None)
            await cls.callback(message, state, *args, **kwargs)

    @classmethod
    async def show(cls, event, state, *args, **kwargs) -> None:
        first_entity = cast(Field, cls.state.get_states()[0].entity)
        await state.set_state(first_entity.state)
        await event.answer(first_entity.label, reply_markup=first_entity.reply_keyboard)

    @classmethod
    async def callback(cls, message: types.Message, state: FSMContext, *args, **kwargs) -> None:
        pass
