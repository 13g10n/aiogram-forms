from unittest.mock import Mock, patch

import pytest

from aiogram_forms.core.states import EntityState, EntityContainerStatesGroup


@pytest.fixture
def container():
    class TestContainer:
        first = Mock()
        second = Mock()
        third = Mock()

        @classmethod
        def filters(cls, *args, **kwargs):
            return {}
    return TestContainer


@pytest.fixture
def container_states_group(container):
    with patch(
            'aiogram_forms.utils.get_attrs_of_type',
            return_value=(
                    ('first', container.first),
                    ('second', container.second),
                    ('third', container.third)
            ),
            autospec=True
    ):
        yield EntityContainerStatesGroup.bind(container)


def test_container_states_group_created(container_states_group):
    assert issubclass(container_states_group, EntityContainerStatesGroup)


def test_container_states_group_get_states(container_states_group):
    assert container_states_group.get_states() == (
        container_states_group.first, container_states_group.second, container_states_group.third
    )


def test_container_states_group_container_assigned(container_states_group, container):
    assert container_states_group.container == container


def test_container_states_group_container_state_assigned(container_states_group, container):
    assert container.state == container_states_group


def test_container_states_group_field_states_assigned(container_states_group, container):
    for key in ['first', 'second', 'third']:
        assert hasattr(container, key)
        assert hasattr(getattr(container, key), 'state')
        assert isinstance(getattr(container, key).state, EntityState)
