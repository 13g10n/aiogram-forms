"""
Forms base implementation.
"""
import inspect
from typing import TYPE_CHECKING, Mapping, Optional, Any, List, Callable, Awaitable, Union, Tuple, Dict

from aiogram import types
from aiogram.filters import Filter

from ..core.entities import Entity, EntityContainer
from ..enums import RouterHandlerType
from ..filters import EntityStatesFilter

if TYPE_CHECKING:
    from ..types import TranslatableString


class Field(Entity):
    """Simple form field implementation."""
    help_text: Optional['TranslatableString']
    error_messages: Mapping[str, 'TranslatableString']
    validators: List[Union[Callable[..., None], Callable[..., Awaitable[None]]]]

    def __init__(
            self,
            label: 'TranslatableString',
            help_text: Optional['TranslatableString'] = None,
            error_messages: Optional[Mapping[str, 'TranslatableString']] = None,
            validators: Optional[List[Union[Callable[..., None], Callable[..., Awaitable[None]]]]] = None
    ) -> None:
        self.label = label
        self.help_text = help_text
        self.error_messages = error_messages or {}
        self.validators = validators or []

    @property
    def reply_keyboard(
            self
    ) -> Union[
        types.InlineKeyboardMarkup,
        types.ReplyKeyboardMarkup,
        types.ReplyKeyboardRemove,
        types.ForceReply,
        None
    ]:
        """Field keyboard."""
        return types.ReplyKeyboardRemove()  # type: ignore[call-arg]

    async def extract(self, message: types.Message) -> Optional[str]:
        """Extract field value from message object."""
        return message.text

    async def process(self, value: Any) -> Any:
        """Process field value format."""
        return value

    async def validate(self, value: Any) -> None:
        """Run validators against processed field value."""
        for validator in self.validators:
            if inspect.iscoroutinefunction(validator):
                await validator(value)
            elif hasattr(validator, '__call__') and inspect.iscoroutinefunction(validator.__call__):
                await validator(value)  # type: ignore[misc]
            else:
                validator(value)


class Form(EntityContainer):
    """Simple form implementation."""

    @classmethod
    def filters(cls, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Mapping[RouterHandlerType, Filter]:
        """Form handler filters."""
        return {
            RouterHandlerType.Message: EntityStatesFilter(cls.state)
        }

    @classmethod
    async def callback(cls, message: types.Message, **data: Dict[str, Any]) -> None:
        """Form completion callback."""
