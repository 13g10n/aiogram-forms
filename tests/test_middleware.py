from unittest.mock import Mock, AsyncMock

import pytest

from aiogram_forms.middleware import EntityMiddleware


@pytest.fixture
def dispatcher():
    return Mock()


@pytest.fixture
def middleware(dispatcher):
    return EntityMiddleware(dispatcher)


@pytest.mark.asyncio
async def test_middleware_call(message, middleware):
    data = {
        'state': Mock()
    }
    handler = AsyncMock(return_value=42)
    assert await middleware(handler, message, data) == 42
