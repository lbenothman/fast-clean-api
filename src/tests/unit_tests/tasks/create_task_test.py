from datetime import datetime, timezone

import pytest

from domain.entities.task import Priority, TaskStatus
from domain.value_objects.create_task_data import CreateTaskData
from use_cases.tasks.create_task_usecase import CreateTaskUseCase


@pytest.fixture
def task_use_case(in_memory_task_repository_fixture):
    use_case = CreateTaskUseCase(in_memory_task_repository_fixture)
    return use_case


@pytest.mark.asyncio
async def test_create_client(task_use_case):
    task_to_create = CreateTaskData(
        title="Test Task",
        description="Test Description",
        priority=Priority.MEDIUM,
        due_date=datetime.now(timezone.utc),
    )

    created_task = await task_use_case.execute(task_to_create)

    assert created_task.title == created_task.title
    assert created_task.description == created_task.description
    assert created_task.status == TaskStatus.PENDING
    assert created_task.priority == created_task.priority
    assert created_task.due_date == created_task.due_date

    assert created_task.id is not None
