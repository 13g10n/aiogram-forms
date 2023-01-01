from unittest.mock import Mock, AsyncMock

import pytest

from aiogram_forms import EntityDispatcher
from aiogram_forms.core.entities import EntityContainer, Entity


@pytest.fixture
def entity_container():
    class TestEntityContainer(EntityContainer):
        first = Entity()
    return TestEntityContainer


@pytest.fixture
def entity_dispatcher():
    return EntityDispatcher()


@pytest.mark.asyncio
async def test_dispatcher_attach_middleware(entity_dispatcher):
    dp = Mock()

    entity_dispatcher.attach(dp)

    dp.message.middleware.assert_called_once()


@pytest.mark.asyncio
async def test_dispatcher_attach_router(entity_dispatcher):
    dp = Mock()

    entity_dispatcher.attach(dp)

    dp.include_router.assert_called_once_with(entity_dispatcher._router)


@pytest.mark.asyncio
async def test_dispatcher_get_entity_container_missing(entity_dispatcher, entity_container):
    with pytest.raises(ValueError):
        entity_dispatcher.get_entity_container(entity_container, 'not existing')


@pytest.mark.asyncio
async def test_dispatcher__get_entity_container_handler_invalid_type(entity_dispatcher, entity_container):
    handler = entity_dispatcher._get_entity_container_handler(entity_container)
    with pytest.raises(RuntimeError):
        await handler(AsyncMock())
