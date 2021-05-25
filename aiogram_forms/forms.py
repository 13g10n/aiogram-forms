from typing import List, Type, Tuple

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message

from aiogram_forms.const import STATES_GROUP_SUFFIX
from aiogram_forms.fields import Field


class FormMeta(type):
    """
    Meta class to handle fields assignments
    """

    def __new__(mcs, name: str, bases: Tuple[Type], namespace: dict, **kwargs: dict) -> Type:
        """
        Class constructor for meta class
        :param name: Subclass name
        :param bases: List of based classes
        :param namespace: Class namespace
        :param kwargs:
        """
        cls = super(FormMeta, mcs).__new__(mcs, name, bases, namespace)

        cls._state = None
        cls._name = name
        cls._fields = mcs._get_form_fields(cls, namespace)

        return cls

    @classmethod
    def _get_form_fields(mcs, form_class: Type, namespace: dict) -> Tuple[Field]:
        """
        Get all Fields for given form
        :param form_class: Form subclass
        :param namespace: Class namespace
        :return:
        """
        fields: List[Field] = []

        for name, prop in namespace.items():
            if isinstance(prop, Field):
                fields.append(prop)
                prop._form = form_class

        return tuple(fields)

    @property
    def state(cls: Type['Form']) -> Type[StatesGroup]:
        """
        Dynamically generated state for fields
        :return:
        """
        if not cls._state:
            cls._state: Type[StatesGroup] = type(
                f'{cls._name}{STATES_GROUP_SUFFIX}',
                (StatesGroup,),
                {
                    field.state_label: State()
                    for field in cls._fields
                }
            )

            for field, state_name in zip(cls._fields, cls._state.states_names):
                field._state = state_name

        return cls._state


class Form(metaclass=FormMeta):
    """
    Base form class
    """
    _name: str = 'Form'
    _fields: Tuple[Field] = tuple()
    _state: Type[StatesGroup] = None

    _registered: bool = False

    @classmethod
    def _register_handler(cls) -> None:
        """
        Register message handlers for form states
        :return:
        """
        if not cls._registered:
            dp: Dispatcher = Dispatcher.get_current()
            dp.register_message_handler(cls._handle_input, state=cls.state.states)
            cls._registered = True

    @classmethod
    async def _handle_input(cls, message: Message, state: FSMContext) -> None:
        """
        Handle form states messages
        :param message: Chat message
        :param state: FSM context
        :return:
        """
        field = await cls.get_current_field()
        if field.validate(message.text):
            await state.update_data(**{field.data_key: message.text})
        else:
            dp = Dispatcher.get_current()
            await dp.bot.send_message(
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
    async def start(cls) -> None:
        """
        Start form processing
        :return:
        """
        cls._register_handler()
        await cls._start_field_promotion(cls._fields[0])

    @classmethod
    async def _start_field_promotion(cls, field: 'Field') -> None:
        """
        Start field processing
        :param field:
        :return:
        """
        dp = Dispatcher.get_current()
        state = Dispatcher.get_current().current_state()
        await state.set_state(field.state)
        await dp.bot.send_message(
            types.Chat.get_current().id,
            text=field.promotion
        )

    @classmethod
    async def get_current_field(cls) -> 'Field':
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
        dp = Dispatcher.get_current()
        state = Dispatcher.get_current().current_state()
        await state.reset_state()
        await dp.bot.send_message(
            types.Chat.get_current().id,
            text='Done'
        )
