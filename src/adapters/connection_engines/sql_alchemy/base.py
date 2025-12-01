from datetime import date, datetime, time
from typing import Any

import sqlalchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from adapters.connection_engines.sql_alchemy.utils.scripts import (
    UPDATED_AT_FUNCTION,
    UPDATED_AT_TRIGGER,
)


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {
        dict: JSONB(none_as_null=True),
        datetime: sqlalchemy.DateTime(timezone=True),
        date: sqlalchemy.DATE,
        time: sqlalchemy.TIME(timezone=True),
    }

    created_at: Mapped[datetime] = mapped_column(
        server_default=sqlalchemy.func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=sqlalchemy.func.current_timestamp(), onupdate=datetime.now()
    )


def create_update_at_trigger(
    target: sqlalchemy.MetaData,
    connection: sqlalchemy.Connection,
    **kwargs: dict[str, Any],
) -> None:
    """
    Creates a PostgreSQL function that automatically sets updated_at to NOW() whenever a row is modified.
    :param target:
    :param connection:
    :param kwargs:
    :return:
    """
    connection.execute(sqlalchemy.DDL(UPDATED_AT_FUNCTION))
    for key in target.tables:
        table = target.tables[key]
        connection.execute(sqlalchemy.DDL(UPDATED_AT_TRIGGER.format(table_name=table)))


sqlalchemy.event.listen(Base.metadata, "after_create", create_update_at_trigger)
