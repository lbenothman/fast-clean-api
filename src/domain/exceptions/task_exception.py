from domain.exceptions.common import EntityNotFound


class TaskException(Exception):
    """Base exception for task-related errors."""

    pass


class TaskNotFound(EntityNotFound):
    """Raised when a task is not found."""

    entity_name = "Task"


class TaskCannotBeCompleted(TaskException):
    """Raised when a task cannot be completed."""

    def __init__(self, task_id: str) -> None:
        self.task_id = task_id
        super().__init__(f"Task with id={task_id} cannot be completed")


class TaskCannotBeDeleted(TaskException):
    """Raised when a task cannot be deleted."""

    def __init__(self, task_id: str) -> None:
        self.task_id = task_id
        super().__init__(f"Task with id={task_id} cannot be deleted")


class TaskUpdateFailed(TaskException):
    """Raised when a task update operation fails."""

    def __init__(self, task_id: str) -> None:
        self.task_id = task_id
        super().__init__(f"Task with id={task_id} could not be updated, please try again")
