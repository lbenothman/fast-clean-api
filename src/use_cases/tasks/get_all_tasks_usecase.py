from typing import Any, Dict

from domain.value_objects.list_entity import ListEntity
from ports.task_repository_interface import TaskRepositoryInterface


class ListAllTasksUseCase:
    def __init__(self, repository: TaskRepositoryInterface):
        self.repository = repository

    async def execute(self, params: Dict[Any, Any]) -> ListEntity:
        tasks = await self.repository.list_all(**params)
        count = await self.repository.count(**params)

        return ListEntity(items=tasks, count=count)
