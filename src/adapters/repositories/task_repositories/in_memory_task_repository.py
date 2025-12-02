from adapters.connection_engines.in_memory_db.in_memory_abstract_repository import (
    InMemoryAbstractRepository,
)
from domain.entities.task import Task
from ports.task_repository_interface import TaskRepositoryInterface


class InMemoryTaskRepository(InMemoryAbstractRepository[Task], TaskRepositoryInterface):
    def _get_filters(self, entity: Task, **filters) -> bool:
        if "id_filter" in filters and entity.id != filters["id_filter"]:
            return False
        if "status_filter" in filters and entity.status != filters["status_filter"]:
            return False
        if (
            "priority_filter" in filters
            and entity.priority != filters["priority_filter"]
        ):
            return False
        return True
