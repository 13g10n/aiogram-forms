"""
Base classes for all components
"""
import abc
from typing import Tuple, Type, List, Optional, Union, Callable, Awaitable, Any, Iterable

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
from babel.support import LazyProxy

from aiogram_forms.const import STATES_GROUP_SUFFIX
from aiogram_forms.errors import FieldValidationError
from aiogram_forms.i18n import i18n


class BaseValidator(abc.ABC):  # pylint: disable=too-few-public-methods
    """Base validator class."""

    @abc.abstractmethod
    async def validate(self, value: str) -> None:
        """
        Validate value provided by user.

        Should raise FieldValidationError with custom message if value not valid.

        :param value: User input
        """


class BaseField(abc.ABC):
    """Base form field."""
    _form: Type['BaseForm']
    _key: str = None
    _state: Type[StatesGroup]

    _label: Union[str, LazyProxy]

    _validators: List[BaseValidator]
    _reply_keyboard: Union[
        ReplyKeyboardRemove,
        ReplyKeyboardMarkup
    ]

    def __init__(
            self,
            label: Union[str, LazyProxy],
            validators: Optional[List[BaseValidator]] = None,
            reply_keyboard: Optional[ReplyKeyboardMarkup] = None,
    ) -> None:
        """
        Base field constructor.

        :param label: field name
        :param validators: list of input validators
        :param reply_keyboard: keyboard to attach
        """
        self._label = label

        self._validators = list(validators) if validators else []
        self._reply_keyboard = reply_keyboard or ReplyKeyboardRemove()

    def __set_name__(self, owner: Type['BaseForm'], name: str) -> None:
        """
        Set field key from parent form
        :param owner: parent form
        :param name: attribute name
        :return: None
        """
        if self._key is None:
            self._key = name
        self._form = owner

    @property
    def state(self) -> Type[StatesGroup]:
        """
        State property
        :return:
        """
        return self._state

    @property
    def label(self) -> str:
        """
        Label property
        :return:
        """
        return self._label

    @property
    def state_label(self) -> str:
        """
        State label property
        :return:
        """
        return f'waiting_{self._key}'

    @property
    def data_key(self) -> str:
        """
        Data key property
        :return:
        """
        return f'{self._form.name}:{self._key}'

    async def validate(self, value: str) -> None:
        """
        Validate field value.

        :param value: User input
        """
        for validator in self._validators:
            await validator.validate(value)


class FormMeta(type):
    """
    Metaclass to handle fields assignments
    """

    def __new__(mcs, name: str, bases: Tuple[Type], namespace: dict, **kwargs: dict) -> Type:  # pylint: disable=unused-argument, bad-mcs-classmethod-argument
        """
        Class constructor for metaclass
        :param name: Subclass name
        :param bases: List of based classes
        :param namespace: Class namespace
        :param kwargs:
        """
        cls = super(FormMeta, mcs).__new__(mcs, name, bases, namespace)

        cls._state = None
        cls.name = name
        cls._fields = mcs._get_form_fields(cls, namespace)

        return cls

    @classmethod
    def _get_form_fields(mcs, form_class: Type, namespace: dict) -> Tuple[BaseField]:  # pylint: disable=bad-mcs-classmethod-argument
        """
        Get all Fields for given form
        :param form_class: Form subclass
        :param namespace: Class namespace
        :return:
        """
        fields: List[BaseField] = []

        for _, prop in namespace.items():
            if isinstance(prop, BaseField):
                fields.append(prop)
                prop._form = form_class  # pylint: disable=protected-access

        return tuple(fields)

    @property
    def state(cls: Type['BaseForm']) -> Type[StatesGroup]:
        """
        Dynamically generated state for fields
        :return:
        """
        if not cls._state:
            cls._state: Type[StatesGroup] = type(
                f'{cls.name}{STATES_GROUP_SUFFIX}',
                (StatesGroup,),
                {
                    field.state_label: State()
                    for field in cls._fields
                }
            )

            for field, state_name in zip(cls._fields, cls._state.states_names):
                field._state = state_name  # pylint: disable=protected-access

        return cls._state


class BaseForm(metaclass=FormMeta):
    """
    Base form class
    """
    name: str = 'Form'
    _fields: Tuple[BaseField] = tuple()
    _state: Type[StatesGroup]

    _registered: bool = False
    _callback: Union[Callable[[Any], Awaitable], Callable[[], Awaitable]] = None
    _callback_args: Iterable[Any] = tuple()

    @classmethod
    def _register_i18n(cls, dispatcher: Dispatcher) -> None:
        """
        Register i18n custom handler.
        """
        i18n.register(dispatcher)

    @classmethod
    def _register_handler(cls, dispatcher: Dispatcher) -> None:
        """
        Register message handlers for form states.
        """
        if not cls._registered:
            dispatcher.register_message_handler(
                cls._handle_input,
                content_types=[
                    types.ContentType.TEXT,
                    types.ContentType.CONTACT
                ],
                state=cls.state.states
            )

            cls._registered = True

    @classmethod
    async def _handle_input(cls, message: types.Message, state: FSMContext) -> None:
        """
        Handle form states messages
        :param message: Chat message
        :param state: FSM context
        :return:
        """
        field = await cls.get_current_field()

        if message.content_type == types.ContentTypes.CONTACT[0]:
            value = message.contact.phone_number
        else:  # types.ContentTypes.TEXT
            value = message.text

        try:
            await field.validate(value)
        except FieldValidationError as validation_error:
            dispatcher = Dispatcher.get_current()
            await dispatcher.bot.send_message(
                types.Chat.get_current().id,
                text=str(validation_error.message)
            )
            return

        await state.update_data(**{field.data_key: value})

        next_field_index = cls._fields.index(field) + 1
        if next_field_index < len(cls._fields):
            await cls._start_field_promotion(cls._fields[next_field_index])
        else:
            await cls.finish()

    @classmethod
    async def start(
            cls,
            callback: Callable[[], Awaitable],
            callback_args: Optional[Iterable[Any]] = None
    ) -> None:
        """
        Start form processing.

        :param callback: Async callback after form processed
        :param callback_args: Args for callback
        """
        if callback:
            cls._callback = callback

        if callback_args:
            cls._callback_args = callback_args

        dispatcher: Dispatcher = Dispatcher.get_current()
        cls._register_i18n(dispatcher)
        cls._register_handler(dispatcher)
        await cls._start_field_promotion(cls._fields[0])

    @classmethod
    async def _start_field_promotion(cls, field: 'BaseField') -> None:
        """
        Start field processing
        :param field:
        :return:
        """
        dispatcher = Dispatcher.get_current()
        state = Dispatcher.get_current().current_state()
        await state.set_state(field.state)
        await dispatcher.bot.send_message(
            types.Chat.get_current().id,
            text=field.label,
            reply_markup=field._reply_keyboard  # pylint: disable=protected-access
        )

    @classmethod
    async def get_current_field(cls) -> 'BaseField':
        """
        Get field which is in processing currently
        :return:
        """
        state = await Dispatcher.get_current().current_state().get_state()
        for field in cls._fields:
            if field.state == state:
                return field

    @classmethod
    async def finish(cls) -> None:
        """
        Finish form processing
        :return:
        """
        state = Dispatcher.get_current().current_state()
        await state.reset_state(with_data=False)
        if cls._callback:
            if cls._callback_args:
                await cls._callback(*cls._callback_args)  # pylint: disable=not-callable
            else:
                await cls._callback()  # pylint: disable=not-callable

    @classmethod
    async def get_data(cls) -> dict:
        """
        Get form data for current user
        :return:
        """
        state = Dispatcher.get_current().current_state()

        async with state.proxy() as data:
            return {
                field.data_key: data.get(field.data_key)
                for field in cls._fields
            }

    @classmethod
    def get_fields(cls) -> Tuple['BaseField']:
        """
        Get form fields.

        :returns: Tuple with form fields
        """
        return cls._fields
