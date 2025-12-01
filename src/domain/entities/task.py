from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from domain.entities.base import EntityBase


class Priority(str, Enum):
    """Task priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, Enum):
    """Task status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task(EntityBase):
    title: str
    description: str
    status: TaskStatus
    priority: Priority
    due_date: datetime | None = None

    def mark_as_completed(self) -> None:
        self.status = TaskStatus.COMPLETED

    def mark_as_in_progress(self) -> None:
        self.status = TaskStatus.IN_PROGRESS

    def is_overdue(self) -> bool:
        if self.due_date is None:
            return False
        return datetime.now() > self.due_date and self.status != TaskStatus.COMPLETED

    def can_be_deleted(self) -> bool:
        return True

    def can_be_completed(self) -> bool:
        return self.status != TaskStatus.COMPLETED
