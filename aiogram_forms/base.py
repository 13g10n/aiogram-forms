"""
Base classes for all components
"""
import abc
from typing import Tuple, Type, List, Optional, Union, Callable, Awaitable

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup

from aiogram_forms.const import STATES_GROUP_SUFFIX


class BaseValidator(abc.ABC):  # pylint: disable=too-few-public-methods
    """
    Base validator class
    """

    @abc.abstractmethod
    async def validate(self, value: str) -> bool:
        """
        Validate value provided by user
        :param value: user input
        :return: bool
        """


class BaseField(abc.ABC):
    """
    Base form field
    """
    _form: Type['BaseForm'] = None
    _key: str = None
    _state = None

    _label: str = None
    _validators: List[BaseValidator] = None
    _reply_keyboard: Optional[Union[
        ReplyKeyboardRemove,
        ReplyKeyboardMarkup
    ]] = None

    def __init__(
            self,
            label: str,
            validators: Optional[List[BaseValidator]] = None,
            reply_keyboard: Optional[ReplyKeyboardMarkup] = None
    ):
        """
        Base field constructor
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
    def state(self):
        """
        State property
        :return:
        """
        return self._state

    @property
    def label(self):
        """
        Label property
        :return:
        """
        return self._label

    @property
    def state_label(self):
        """
        State label property
        :return:
        """
        return f'waiting_{self._key}'

    @property
    def data_key(self):
        """
        Data key property
        :return:
        """
        return f'{self._form.name}:{self._key}'

    async def validate(self, value) -> bool:
        """
        Validate field value
        :param value: user input
        :return:
        """
        for validator in self._validators:
            if not await validator.validate(value):
                return False
        return True


class FormMeta(type):
    """
    Meta class to handle fields assignments
    """

    def __new__(mcs, name: str, bases: Tuple[Type], namespace: dict, **kwargs: dict) -> Type:  # pylint: disable=unused-argument, bad-mcs-classmethod-argument
        """
        Class constructor for meta class
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
    _state: Type[StatesGroup] = None

    _registered: bool = False
    _callback: Callable[[], Awaitable] = None

    @classmethod
    def _register_handler(cls) -> None:
        """
        Register message handlers for form states
        :return:
        """
        if not cls._registered:
            dispatcher: Dispatcher = Dispatcher.get_current()
            dispatcher.register_message_handler(cls._handle_input, state=cls.state.states)
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
        if await field.validate(message.text):
            await state.update_data(**{field.data_key: message.text})
        else:
            dispatcher = Dispatcher.get_current()
            await dispatcher.bot.send_message(
                types.Chat.get_current().id,
                text='Invalid value, try again'
            )
            return

        next_field_index = cls._fields.index(field) + 1
        if next_field_index < len(cls._fields):
            await cls._start_field_promotion(cls._fields[next_field_index])
        else:
            await cls.finish()

    @classmethod
    async def start(cls, callback: Callable[[], Awaitable]) -> None:
        """
        Start form processing
        :return:
        """
        if callback:
            cls._callback = callback

        cls._register_handler()
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
