import pytest

from aiogram_forms.utils import get_attrs_of_type


@pytest.fixture
def example_class():
    class Example:
        foo = 42
        bar = 'value'
        another = 'too'
        exp = object()
    return Example


def test_get_attrs_of_type(example_class):
    assert get_attrs_of_type(example_class, str) == (('bar', 'value'), ('another', 'too'))
