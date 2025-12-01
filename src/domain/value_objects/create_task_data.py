from dataclasses import dataclass
from datetime import datetime

from domain.entities.task import Priority


@dataclass
class CreateTaskData:
    title: str
    description: str
    priority: Priority
    due_date: datetime | None = None
