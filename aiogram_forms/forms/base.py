import abc
from typing import TYPE_CHECKING, Mapping, cast, List, Optional

from aiogram import types
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext

from .errors import FieldValidationError
from ..base import Entity, EntityContainer
from ..enums import RouterHandlerType
from ..filters import EntityStatesFilter

if TYPE_CHECKING:
    from ..states import EntityState


class Validator(abc.ABC):
    """Base validator class."""

    @abc.abstractmethod
    async def validate(self, value: str) -> None:
        """
        Validate value provided by user.
        Should raise FieldValidationError with custom message if value not valid.

        :param value: User input
        """


class Field(Entity):
    _validators: List[Validator]

    def __init__(
            self,
            label: str,
            validators: Optional[List[Validator]] = None
    ) -> None:
        self.label = label
        self._validators = validators or []

    @property
    def reply_keyboard(self):
        return types.ReplyKeyboardRemove()

    async def validate(self, value: str) -> None:
        for validator in self._validators:
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
            await field.validate(message.text)
        except FieldValidationError as error:
            await message.answer(error.message, reply_markup=field.reply_keyboard)
            return

        # TODO: save to state

        next_entity: Field = cast(Field, current_state.entity.next)
        if next_entity:
            await state.set_state(next_entity.state)
            await message.answer(next_entity.label, reply_markup=next_entity.reply_keyboard)
        else:
            await state.set_state(None)

    @classmethod
    async def show(cls, message, state, *args, **kwargs) -> None:
        first_entity = cast(Field, cls.state.get_states()[0].entity)
        await state.set_state(first_entity.state)
        await message.answer(first_entity.label, reply_markup=first_entity.reply_keyboard)
