from uuid import uuid4

import pytest

from domain.entities.task import TaskStatus
from domain.exceptions.task_exception import TaskCannotBeCompleted, TaskNotFound
from use_cases.tasks.complete_task_usecase import CompleteTaskUseCase


@pytest.fixture
def complete_task_use_case(in_memory_task_repository_fixture):
    use_case = CompleteTaskUseCase(in_memory_task_repository_fixture)
    return use_case


@pytest.mark.asyncio
async def test_complete_pending_task_successfully(
    complete_task_use_case, pending_task_fixture
):
    completed_task = await complete_task_use_case.execute(pending_task_fixture.id)

    assert completed_task.status == TaskStatus.COMPLETED
    assert completed_task.id == pending_task_fixture.id
    assert completed_task.title == pending_task_fixture.title


@pytest.mark.asyncio
async def test_complete_in_progress_task_successfully(
    complete_task_use_case, in_progress_task_fixture
):
    completed_task = await complete_task_use_case.execute(in_progress_task_fixture.id)

    assert completed_task.status == TaskStatus.COMPLETED
    assert completed_task.id == in_progress_task_fixture.id


@pytest.mark.asyncio
async def test_complete_task_not_found(complete_task_use_case):
    non_existent_task_id = uuid4()

    with pytest.raises(TaskNotFound) as exc_info:
        await complete_task_use_case.execute(non_existent_task_id)

    assert str(non_existent_task_id) in str(exc_info.value)


@pytest.mark.asyncio
async def test_complete_already_completed_task_raises_exception(
    complete_task_use_case, completed_task_fixture
):
    with pytest.raises(TaskCannotBeCompleted) as exc_info:
        await complete_task_use_case.execute(completed_task_fixture.id)

    assert str(completed_task_fixture.id) in str(exc_info.value)
