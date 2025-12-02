from uuid import UUID

from domain.entities.task import Task
from domain.exceptions.task_exception import TaskCannotBeCompleted, TaskNotFound
from ports.task_repository_interface import TaskRepositoryInterface


class CompleteTaskUseCase:
    def __init__(self, repository: TaskRepositoryInterface):
        self.repository = repository

    async def execute(self, task_id: UUID) -> Task:
        task = await self.repository.get(id_filter=task_id)

        if task is None:
            raise TaskNotFound(str(task_id))

        if not task.can_be_completed():
            raise TaskCannotBeCompleted(str(task_id))

        task.mark_as_completed()
        updated_count = await self.repository.update(
            fields_to_update={"status": task.status}
        )

        if updated_count == 0:
            raise TaskNotFound(str(task_id))

        return task
