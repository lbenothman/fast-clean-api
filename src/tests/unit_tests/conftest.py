import pytest_asyncio

from adapters.repositories.task_repositories.in_memory_task_repository import (
    InMemoryTaskRepository,
)
from domain.entities.task import Priority, Task, TaskStatus
from tests.utilis import create_task


@pytest_asyncio.fixture()
async def in_memory_task_repository_fixture():
    return InMemoryTaskRepository()


@pytest_asyncio.fixture()
async def client_1_fixture(in_memory_client_repository_fixture) -> Task:
    task = create_task(index=1)
    return await in_memory_client_repository_fixture.save(task)


@pytest_asyncio.fixture()
async def pending_task_fixture(in_memory_task_repository_fixture) -> Task:
    task = create_task(index=1, status=TaskStatus.PENDING)
    return await in_memory_task_repository_fixture.save(task)


@pytest_asyncio.fixture()
async def in_progress_task_fixture(in_memory_task_repository_fixture) -> Task:
    task = create_task(index=2, status=TaskStatus.IN_PROGRESS)
    return await in_memory_task_repository_fixture.save(task)


@pytest_asyncio.fixture()
async def completed_task_fixture(in_memory_task_repository_fixture) -> Task:
    task = create_task(index=3, status=TaskStatus.COMPLETED, priority=Priority.LOW)
    return await in_memory_task_repository_fixture.save(task)
