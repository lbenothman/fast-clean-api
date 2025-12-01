from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.task import Task
from domain.value_objects.ordering import Ordering
from typing import Any

class TaskRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, task: Task) -> Task:
        pass

    async def get(
        self,
        **filters,
    ) -> Task | None:
        pass

    @abstractmethod
    async def list_all(
        self,
        page: int = 1,
        limit: int = 10,
        order_by: str = "created_at",
        ordering: Ordering = Ordering.ASC,
        **filters,
    ) -> list[Task]:
        pass

    @abstractmethod
    async def count(
        self,
        **filters,
    ) -> int:
        pass

    @abstractmethod
    async def update(
        self,
        fields_to_update: dict[str, Any],
        **filters,
    ) -> int:
        pass

    @abstractmethod
    async def delete(
        self,
        **filters,
    ) -> int:
        pass
