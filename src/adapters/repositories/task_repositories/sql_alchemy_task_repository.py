from typing import Any, List

from adapters.connection_engines.sql_alchemy.models import TaskModel
from adapters.connection_engines.sql_alchemy.SqlAlchemyAbstractRepository import (
    SqlAlchemyAbstractRepository,
)
from domain.entities.task import Priority, Task, TaskStatus
from ports.task_repository_interface import TaskRepositoryInterface


class SqlAlchemyTaskRepository(
    SqlAlchemyAbstractRepository[Task, TaskModel], TaskRepositoryInterface
):
    model = TaskModel

    def _get_filters(self, **filters) -> List[Any]:
        conditions = []
        if "id_filter" in filters:
            conditions.append(TaskModel.id == filters["id_filter"])
        if "status_filter" in filters:
            conditions.append(TaskModel.status == filters["status_filter"])
        if "priority_filter" in filters:
            conditions.append(TaskModel.priority == filters["priority_filter"])

        return conditions

    @staticmethod
    def _model_to_entity(task_model: TaskModel) -> Task:
        return Task(
            id=task_model.id,
            title=task_model.title,
            description=task_model.description,
            status=TaskStatus(task_model.status),
            priority=Priority(task_model.priority),
            due_date=task_model.due_date,
            created_at=task_model.created_at,
            updated_at=task_model.updated_at,
        )

    @staticmethod
    def _entity_to_model(entity: Task) -> TaskModel:
        return TaskModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            status=TaskStatus(entity.status),
            priority=Priority(entity.priority),
            due_date=entity.due_date,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
