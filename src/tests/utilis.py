from datetime import datetime, timedelta, timezone

from sqlalchemy import text

from adapters.connection_engines.sql_alchemy.models import TaskModel
from domain.entities.task import Priority, Task, TaskStatus


def create_task(
    index: int, status=TaskStatus.PENDING, priority=Priority.MEDIUM
) -> Task:
    now = datetime.now(timezone.utc)

    return Task(
        id=None,
        title=f"My task {index}",
        description=f"This is my task {index}",
        status=status,
        priority=priority,
        due_date=now + timedelta(hours=index),
        created_at=now,
        updated_at=now,
    )


async def truncate_tables(db_session):
    table_names = [
        TaskModel.__tablename__,
    ]

    for table in table_names:
        await db_session.execute(text(f"DELETE FROM {table};"))

    await db_session.commit()
