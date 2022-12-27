"""
Core entity states.
"""
from typing import Type, cast, Tuple

from aiogram.fsm.state import StatesGroup, State

from .entities import EntityContainer, Entity
from ..const import STATES_GROUP_CLASS_SUFFIX
from .. import utils


class EntityState(State):
    """Entity state."""
    entity: 'Entity'

    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity


class EntityContainerStatesGroup(StatesGroup):
    """Entity container states group."""
    container: Type['EntityContainer']

    @classmethod
    def get_states(cls) -> Tuple[EntityState]:
        """Get all entity container states."""
        return cast(
            Tuple[EntityState],
            cls.__states__  # pylint: disable=no-member
        )

    @classmethod
    def bind(cls, container: Type['EntityContainer']) -> Type['EntityContainerStatesGroup']:
        """Create and bind entity container states group."""
        form_fields = utils.get_attrs_of_type(container, Entity)

        state_class = cast(
            Type[EntityContainerStatesGroup],
            type(
                f'{container.__name__}{STATES_GROUP_CLASS_SUFFIX}',
                (EntityContainerStatesGroup,),
                {
                    key: EntityState(value)
                    for key, value in form_fields
                }
            )
        )

        for key, value in form_fields:
            value.state = getattr(state_class, key)

        container.state = state_class
        state_class.container = container

        return state_class
