from typing import Mapping, Optional, Any, List, Callable

from aiogram import types
from aiogram.filters import Filter

from ..core.entities import Entity, EntityContainer
from ..enums import RouterHandlerType
from ..filters import EntityStatesFilter


class Field(Entity):
    """Simple form field implementation."""
    help_text: Optional[str]
    error_messages: Optional[Mapping[str, str]]
    validators: List[Callable]

    def __init__(
            self,
            label: str,
            help_text: Optional[str] = None,
            error_messages: Optional[Mapping[str, str]] = None,
            validators: Optional[list] = None
    ) -> None:
        self.label = label
        self.help_text = help_text
        self.error_messages = error_messages
        self.validators = validators or []

    @property
    def reply_keyboard(self):
        return types.ReplyKeyboardRemove()

    async def extract(self, message: types.Message) -> Any:
        """Extract field value from message object."""
        # TODO: other types:
        # if message.content_type == 'contact':
        #     await field.validate(message.contact.phone_number)
        return message.text

    async def process(self, value: Any) -> Any:
        """Process field value format."""
        return value

    async def validate(self, value: Any) -> None:
        """Run validators against processed field value."""
        for validator in self.validators:
            await validator(value)


class Form(EntityContainer):
    """Simple form implementation."""

    @classmethod
    def filters(cls, *args, **kwargs) -> Mapping[RouterHandlerType, Filter]:
        return {
            RouterHandlerType.Message: EntityStatesFilter(cls.state)
        }
