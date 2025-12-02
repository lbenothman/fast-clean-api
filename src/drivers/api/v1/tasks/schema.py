from datetime import datetime
from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.task import Priority, TaskStatus
from drivers.helpers.hetoas import ListingParams


class CreateTaskRequest(BaseModel):
    """Request model for creating a new task."""

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str = Field(..., min_length=1, description="Task description")
    priority: Priority = Field(..., description="Task priority")
    due_date: datetime | None = Field(None, description="Task due date")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for the FastAPI Clean Architecture tutorial",
                "priority": "high",
                "due_date": "2024-12-31T23:59:59Z",
            }
        }


class UpdateTaskRequest(BaseModel):
    """Request model for updating a task."""

    title: str | None = Field(
        None, min_length=1, max_length=200, description="Task title"
    )
    description: str | None = Field(None, min_length=1, description="Task description")
    status: TaskStatus | None = Field(None, description="Task status")
    priority: Priority | None = Field(None, description="Task priority")
    due_date: datetime | None = Field(None, description="Task due date")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated task title",
                "description": "Updated task description",
                "status": "in_progress",
                "priority": "medium",
            }
        }


class TaskResponse(BaseModel):
    """Response model for a task."""

    id: UUID = Field(..., description="Task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    status: TaskStatus = Field(..., description="Task status")
    priority: Priority = Field(..., description="Task priority")
    due_date: datetime | None = Field(None, description="Task due date")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for the FastAPI Clean Architecture tutorial",
                "status": "pending",
                "priority": "high",
                "due_date": "2024-12-31T23:59:59Z",
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z",
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str = Field(..., description="Error message")


class TaskListParams(ListingParams):
    status_filter: TaskStatus | None = None
    priority_filter: Priority | None = None


class TaskListResponse(BaseModel):
    items: list[TaskResponse] = Field(..., description="List of tasks")
    total_count: int = Field(..., description="Total number of tasks")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Number of items per page")
    links: Dict[str, Any] = Field(..., description="HATEOAS pagination links")
