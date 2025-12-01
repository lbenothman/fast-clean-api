import pytest
from httpx import AsyncClient

from domain.entities.task import Task, TaskStatus


@pytest.mark.asyncio
async def test_complete_task_success(
    async_client_fixture: AsyncClient,
        pending_task_with_medium_priority_fixture: Task
):
    response = await async_client_fixture.patch(
        f"/api/v1/tasks/{pending_task_with_medium_priority_fixture.id}/complete",
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(pending_task_with_medium_priority_fixture.id)
    assert data["title"] == pending_task_with_medium_priority_fixture.title
    assert data["description"] == pending_task_with_medium_priority_fixture.description
    assert data["status"] == TaskStatus.COMPLETED.value
    assert data["priority"] == pending_task_with_medium_priority_fixture.priority.value


@pytest.mark.asyncio
async def test_complete_task_not_found(
    async_client_fixture: AsyncClient,
):
    non_existent_task_id = "00000000-0000-0000-0000-000000000000"

    response = await async_client_fixture.patch(
        f"/api/v1/tasks/{non_existent_task_id}/complete",
    )

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_complete_already_completed_task(
    async_client_fixture: AsyncClient,
        completed_task_with_low_priority_fixture: Task
):
    response = await async_client_fixture.patch(
        f"/api/v1/tasks/{completed_task_with_low_priority_fixture.id}/complete",
    )

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_complete_task_invalid_uuid(
    async_client_fixture: AsyncClient,
):
    invalid_task_id = "invalid-uuid"

    response = await async_client_fixture.patch(
        f"/api/v1/tasks/{invalid_task_id}/complete",
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
