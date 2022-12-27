from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def message():
    return AsyncMock(text='Test message.')


@pytest.fixture
def contact_message():
    return AsyncMock(text='Test message.', content_type='contact')
