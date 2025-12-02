import pytest
from httpx import AsyncClient

from domain.entities.task import Priority, TaskStatus


@pytest.mark.asyncio
async def test_list_all_tasks_empty(async_client_fixture: AsyncClient):
    response = await async_client_fixture.get("/api/v1/tasks")

    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total_count"] == 0
    assert "page" in data
    assert "limit" in data
    assert "links" in data


@pytest.mark.asyncio
async def test_list_all_tasks_with_single_task(
    async_client_fixture: AsyncClient, pending_task_with_medium_priority_fixture
):
    response = await async_client_fixture.get("/api/v1/tasks")

    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == str(pending_task_with_medium_priority_fixture.id)
    assert data["items"][0]["title"] == pending_task_with_medium_priority_fixture.title
    assert (
        data["items"][0]["description"]
        == pending_task_with_medium_priority_fixture.description
    )
    assert (
        data["items"][0]["status"]
        == pending_task_with_medium_priority_fixture.status.value
    )
    assert (
        data["items"][0]["priority"]
        == pending_task_with_medium_priority_fixture.priority.value
    )
    assert "page" in data
    assert "limit" in data
    assert "links" in data


@pytest.mark.asyncio
async def test_list_all_tasks_with_multiple_tasks(
    async_client_fixture: AsyncClient,
    pending_task_with_medium_priority_fixture,
    completed_task_with_low_priority_fixture,
):
    response = await async_client_fixture.get("/api/v1/tasks")

    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 2
    assert len(data["items"]) == 2

    task_ids = {task["id"] for task in data["items"]}
    assert str(pending_task_with_medium_priority_fixture.id) in task_ids
    assert str(completed_task_with_low_priority_fixture.id) in task_ids
    assert "page" in data
    assert "limit" in data
    assert "links" in data


@pytest.mark.asyncio
async def test_list_all_tasks_filter_by_status(
    async_client_fixture: AsyncClient,
    pending_task_with_medium_priority_fixture,
    completed_task_with_low_priority_fixture,
):
    response = await async_client_fixture.get(
        "/api/v1/tasks", params={"status_filter": TaskStatus.COMPLETED.value}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == str(completed_task_with_low_priority_fixture.id)
    assert data["items"][0]["status"] == TaskStatus.COMPLETED.value
    assert "page" in data
    assert "limit" in data
    assert "links" in data


@pytest.mark.asyncio
async def test_list_all_tasks_filter_by_priority(
    async_client_fixture: AsyncClient,
    pending_task_with_medium_priority_fixture,
    completed_task_with_low_priority_fixture,
):
    response = await async_client_fixture.get(
        "/api/v1/tasks", params={"priority_filter": Priority.MEDIUM.value}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["priority"] == Priority.MEDIUM.value
    assert "page" in data
    assert "limit" in data
    assert "links" in data


@pytest.mark.asyncio
async def test_list_all_tasks_filter_by_status_and_priority(
    async_client_fixture: AsyncClient,
    pending_task_with_medium_priority_fixture,
    completed_task_with_low_priority_fixture,
):
    response = await async_client_fixture.get(
        "/api/v1/tasks",
        params={
            "status_filter": TaskStatus.COMPLETED.value,
            "priority_filter": Priority.LOW.value,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == str(completed_task_with_low_priority_fixture.id)
    assert data["items"][0]["status"] == TaskStatus.COMPLETED.value
    assert data["items"][0]["priority"] == Priority.LOW.value
    assert "page" in data
    assert "limit" in data
    assert "links" in data


@pytest.mark.asyncio
async def test_list_all_tasks_with_pagination(
    async_client_fixture: AsyncClient,
    pending_task_with_medium_priority_fixture,
    completed_task_with_low_priority_fixture,
):
    response = await async_client_fixture.get(
        "/api/v1/tasks", params={"page": 1, "limit": 1}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 2
    assert len(data["items"]) == 1
    assert data["page"] == 1
    assert data["limit"] == 1
    assert "links" in data
