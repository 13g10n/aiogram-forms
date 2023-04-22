"""
Form fields.
"""
from typing import Optional, Any, Dict, TYPE_CHECKING, Tuple, Union, Iterable

from aiogram import types
from aiogram.utils.i18n.lazy_proxy import LazyProxy  # type: ignore[attr-defined]

from .base import Field
from . import validators

if TYPE_CHECKING:
    from ..types import TranslatableString


class TextField(Field):
    """Simple text field."""

    def __init__(
            self,
            *args: Tuple[Any],
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            **kwargs: Dict[str, Any]
    ) -> None:
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(max_length))


class EmailField(Field):
    """Email field."""

    def __init__(self, label: 'TranslatableString', *args: Tuple[Any], **kwargs: Dict[str, Any]) -> None:
        super().__init__(label, *args, **kwargs)  # type: ignore[arg-type]
        self.validators.append(validators.EmailValidator())


class PhoneNumberField(Field):
    """Phone number field."""

    def __init__(
            self,
            label: 'TranslatableString',
            *args: Tuple[Any],
            share_contact: Optional[bool] = False,
            **kwargs: Dict[str, Any]
    ) -> None:
        super().__init__(label, *args, **kwargs)  # type: ignore[arg-type]
        self.share_contact = share_contact
        self.validators.append(validators.PhoneNumberValidator())

    @property
    def reply_keyboard(self) -> Union[
        types.InlineKeyboardMarkup,
        types.ReplyKeyboardMarkup,
        types.ReplyKeyboardRemove,
        types.ForceReply,
        None
    ]:
        if self.share_contact:
            return types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text=str(self.label), request_contact=True)]
                ],
                resize_keyboard=True
            )
        return super().reply_keyboard

    async def extract(self, message: types.Message) -> Optional[str]:
        if message.content_type == 'contact':
            return message.contact.phone_number  # type: ignore[union-attr]
        return await super().extract(message)


class ChoiceField(Field):
    """Choices field."""

    def __init__(
            self,
            label: 'TranslatableString',
            *args: Tuple[Any],
            choices: Iterable[Tuple['TranslatableString', Any]],
            **kwargs: Dict[str, Any]
    ) -> None:
        super().__init__(label, *args, **kwargs)  # type: ignore[arg-type]
        self.choices = choices
        self.validators.append(
            validators.ChoiceValidator(choices=tuple(
                map(lambda x: x[1], choices)
            ))
        )

    async def process(self, value: str) -> Any:
        for label, key in self.choices:
            if value == label:
                return key
        return None

    @property
    def reply_keyboard(self) -> types.ReplyKeyboardMarkup:
        return types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text=label.value if isinstance(label, LazyProxy) else label)]
                for label, option in self.choices
            ],
            resize_keyboard=True
        )
