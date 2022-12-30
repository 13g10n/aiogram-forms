from unittest.mock import Mock

import pytest
from aiogram.filters import Filter

from aiogram_forms.enums import RouterHandlerType
from aiogram_forms.forms.base import Field, Form


@pytest.fixture
def form_class():
    class TestForm(Form):
        first = Field('First')
    return TestForm


def test_form_creation(form_class):
    assert issubclass(form_class, Form)


def test_form_default_filter(form_class):
    filters = form_class.filters()
    assert isinstance(filters, dict)
    assert RouterHandlerType.Message in filters
    assert all(isinstance(filters[filter_type], Filter) for filter_type in filters)


@pytest.mark.asyncio
async def test_form_callback_callable(form_class):
    await form_class.callback(Mock())
