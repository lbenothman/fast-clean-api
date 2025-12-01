import logging
from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from adapters.connection_engines.sql_alchemy.session import get_session_maker
from drivers.config.settings import get_settings

logger = logging.getLogger("db")


class SqlAlchemySessionMaker:
    def __init__(self) -> None:
        self._engine: async_sessionmaker[AsyncSession | Any] | None = None

    def __call__(self, settings=Depends(get_settings)):
        if self._engine is not None:
            logger.info("Get the engine from the cache")
            return self._engine

        logger.info("Create SQLAlchemy engine")
        self._engine = get_session_maker(settings)
        return self._engine


sqlAlchemySessionMaker = SqlAlchemySessionMaker()


async def get_db_session(
    engine: SqlAlchemySessionMaker = Depends(sqlAlchemySessionMaker),
) -> AsyncGenerator[AsyncSession, None]:
    async with engine() as session, session.begin():
        yield session
