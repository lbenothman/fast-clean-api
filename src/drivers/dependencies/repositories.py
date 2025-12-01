from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repositories.task_repositories.sql_alchemy_task_repository import (
    SqlAlchemyTaskRepository,
)
from drivers.dependencies.database import get_db_session


def get_task_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> SqlAlchemyTaskRepository:
    return SqlAlchemyTaskRepository(db_session)
