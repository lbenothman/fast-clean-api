import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from adapters.repositories.task_repositories.sql_alchemy_task_repository import (
    SqlAlchemyTaskRepository,
)
from domain.entities.task import Priority, Task, TaskStatus
from drivers.main import app
from tests.utilis import create_task, truncate_tables


@pytest_asyncio.fixture(autouse=True, scope="function")
async def truncate_all_tables(db_session_fixture):
    yield
    await truncate_tables(db_session_fixture)


@pytest_asyncio.fixture
async def async_client_fixture():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def task_repository_fixture(db_session_fixture) -> SqlAlchemyTaskRepository:
    return SqlAlchemyTaskRepository(db_session_fixture)


@pytest_asyncio.fixture()
async def pending_task_with_medium_priority_fixture(
    task_repository_fixture, db_session_fixture
) -> Task:
    task = await task_repository_fixture.save(entity=create_task(index=1))
    await db_session_fixture.commit()
    return task


@pytest_asyncio.fixture()
async def completed_task_with_low_priority_fixture(
    task_repository_fixture, db_session_fixture
) -> Task:
    task = await task_repository_fixture.save(
        entity=create_task(index=2, status=TaskStatus.COMPLETED, priority=Priority.LOW)
    )
    await db_session_fixture.commit()
    return task
