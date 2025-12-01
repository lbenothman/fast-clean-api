import pytest

from domain.entities.task import Priority, TaskStatus
from use_cases.tasks.get_all_tasks_usecase import ListAllTasksUseCase


@pytest.fixture
def list_all_tasks_use_case(in_memory_task_repository_fixture):
    use_case = ListAllTasksUseCase(in_memory_task_repository_fixture)
    return use_case


@pytest.mark.asyncio
async def test_list_all_tasks_empty_repository(list_all_tasks_use_case):
    result = await list_all_tasks_use_case.execute({})

    assert result.count == 0
    assert result.items == []


@pytest.mark.asyncio
async def test_list_all_tasks_with_single_task(
    list_all_tasks_use_case, pending_task_fixture
):
    result = await list_all_tasks_use_case.execute({})

    assert result.count == 1
    assert len(result.items) == 1
    assert result.items[0].id == pending_task_fixture.id
    assert result.items[0].title == pending_task_fixture.title


@pytest.mark.asyncio
async def test_list_all_tasks_with_multiple_tasks(
    list_all_tasks_use_case,
    pending_task_fixture,
    in_progress_task_fixture,
    completed_task_fixture,
):
    result = await list_all_tasks_use_case.execute({})

    assert result.count == 3
    assert len(result.items) == 3

    task_ids = {task.id for task in result.items}
    assert pending_task_fixture.id in task_ids
    assert in_progress_task_fixture.id in task_ids
    assert completed_task_fixture.id in task_ids


@pytest.mark.asyncio
async def test_list_all_tasks_with_params(
    list_all_tasks_use_case,
    pending_task_fixture,
    in_progress_task_fixture,
):
    params = {"limit": 1}
    result = await list_all_tasks_use_case.execute(params)

    assert result.count == 2
    assert len(result.items) == 1


@pytest.mark.asyncio
async def test_list_all_tasks_filter_by_status(
    list_all_tasks_use_case,
    pending_task_fixture,
    in_progress_task_fixture,
    completed_task_fixture,
):
    params = {"status_filter": TaskStatus.PENDING}
    result = await list_all_tasks_use_case.execute(params)

    assert result.count == 1
    assert len(result.items) == 1
    assert result.items[0].id == pending_task_fixture.id
    assert result.items[0].status == TaskStatus.PENDING


@pytest.mark.asyncio
async def test_list_all_tasks_filter_by_priority(
    list_all_tasks_use_case,
    pending_task_fixture,
    in_progress_task_fixture,
    completed_task_fixture,
):
    params = {"priority_filter": Priority.LOW}
    result = await list_all_tasks_use_case.execute(params)

    assert result.count == 1
    assert len(result.items) == 1
    assert result.items[0].id == completed_task_fixture.id
    assert result.items[0].priority == Priority.LOW


@pytest.mark.asyncio
async def test_list_all_tasks_filter_by_status_and_priority(
    list_all_tasks_use_case,
    pending_task_fixture,
    in_progress_task_fixture,
    completed_task_fixture,
):
    params = {"status_filter": TaskStatus.COMPLETED, "priority_filter": Priority.LOW}
    result = await list_all_tasks_use_case.execute(params)

    assert result.count == 1
    assert len(result.items) == 1
    assert result.items[0].id == completed_task_fixture.id
    assert result.items[0].status == TaskStatus.COMPLETED
    assert result.items[0].priority == Priority.LOW
