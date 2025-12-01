from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from drivers.config.settings import BaseSettings


def get_session_maker(settings: BaseSettings) -> async_sessionmaker[AsyncSession | Any]:
    engine = create_async_engine(settings.database_url, echo=True)

    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
