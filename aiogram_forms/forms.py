from typing import List, Type

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message

from aiogram_forms.fields import Field


class FormMeta(type):
    _state: Type[StatesGroup]

    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super(FormMeta, mcs).__new__(mcs, name, bases, namespace)

        cls._name = name

        fields: List[Field] = []

        for name, prop in namespace.items():
            if isinstance(prop, Field):
                fields.append(prop)
                prop._form = cls

        cls._fields = tuple(fields)
        cls._state = None

        return cls

    @property
    def state(cls):
        if not cls._state and cls._fields:
            cls._state = type(
                f'{cls._name}StatesGroup',
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
    _name: str
    _fields: list
    _state: Type[StatesGroup]

    __registered: bool = False

    @classmethod
    def _register_handler(cls):
        if not cls.__registered:
            dp: Dispatcher = Dispatcher.get_current()
            dp.register_message_handler(cls._handle_input, state=cls.state.states)
            cls.__registered = True

    @classmethod
    async def _handle_input(cls, message: Message, state: FSMContext):
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
    async def start(cls):
        cls._register_handler()
        await cls._start_field_promotion(cls._fields[0])

    @classmethod
    async def _start_field_promotion(cls, field: 'Field'):
        dp = Dispatcher.get_current()
        state = Dispatcher.get_current().current_state()
        await state.set_state(field.state)
        await dp.bot.send_message(
            types.Chat.get_current().id,
            text=field.promotion
        )

    @classmethod
    async def get_current_field(cls) -> 'Field':
        state = await Dispatcher.get_current().current_state().get_state()
        for field in cls._fields:
            if field.state == state:
                return field

    @classmethod
    async def finish(cls):
        dp = Dispatcher.get_current()
        state = Dispatcher.get_current().current_state()
        await state.reset_state()
        await dp.bot.send_message(
            types.Chat.get_current().id,
            text='Done'
        )
