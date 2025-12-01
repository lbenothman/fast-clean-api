from datetime import datetime, timezone
from uuid import uuid4

from domain.entities.task import Task, TaskStatus
from domain.value_objects.create_task_data import CreateTaskData
from ports.task_repository_interface import TaskRepositoryInterface


class CreateTaskUseCase:
    def __init__(self, repository: TaskRepositoryInterface):
        self.repository = repository

    async def execute(self, data: CreateTaskData) -> Task:
        task = Task(
            id=uuid4(),
            title=data.title,
            description=data.description,
            status=TaskStatus.PENDING,
            priority=data.priority,
            due_date=data.due_date,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        return await self.repository.save(task)
