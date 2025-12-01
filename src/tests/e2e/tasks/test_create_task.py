import pytest
from httpx import AsyncClient

from domain.entities.task import TaskStatus


@pytest.mark.asyncio
async def test_create_client_success(
    async_client_fixture: AsyncClient
):
    new_client = {
        "title": "My task title",
        "description": "This is my task description",
        "priority": "low",
        "due_date": "2027-01-01T00:00:00Z"
    }

    # Inject JWT token via headers
    response = await async_client_fixture.post(
        "/api/v1/tasks",
        json=new_client,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == new_client["title"]
    assert data["description"] == new_client["description"]
    assert data["priority"] == new_client["priority"]
    assert data["status"] == TaskStatus.PENDING.value
    assert "id" in data
