from abc import ABC, abstractmethod
from typing import Any, Generic, List, TypeVar

import sqlalchemy
from sqlalchemy import asc, desc, func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.connection_engines.sql_alchemy.models import Base
from domain.entities.base import EntityBase
from domain.exceptions.common import DatabaseException
from domain.value_objects.ordering import Ordering

Entity = TypeVar("Entity", bound=EntityBase)
SqlAlchemyModel = TypeVar("SqlAlchemyModel", bound=Base)


class SqlAlchemyAbstractRepository(ABC, Generic[Entity, SqlAlchemyModel]):
    # The SQLAlchemy model class (not instance) used by this repository
    model: type[SqlAlchemyModel]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: Entity) -> Entity:
        model = self._entity_to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)

        return self._model_to_entity(model)

    async def update(
        self,
        fields_to_update: dict[str, Any],
        **filters,
    ) -> int:
        try:
            filter_conditions = self._get_filters(**filters)

            query = (
                sqlalchemy.update(self.model)
                .where(*filter_conditions)
                .values(fields_to_update)
            )

            result = await self._session.execute(query)
            await self._session.flush()
            return result.rowcount  # type: ignore[attr-defined]
        except IntegrityError as exception:
            await self._session.rollback()
            raise exception
        except SQLAlchemyError as exception:
            await self._session.rollback()
            raise DatabaseException from exception

    async def list_all(
        self,
        page: int = 1,
        limit: int = 10,
        order_by: str = "created_at",
        ordering: Ordering = Ordering.ASC,
        **filters,
    ) -> List[Entity]:
        query = select(self.model)

        filter_conditions = self._get_filters(**filters)
        query = query.where(*filter_conditions)

        query.order_by(self._get_order_expression(order_by=order_by, ordering=ordering))
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        result = await self._session.execute(query)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def get(
        self,
        **filters,
    ) -> Entity | None:
        query = select(self.model)

        filter_conditions = self._get_filters(**filters)
        query = query.where(*filter_conditions)
        model = await self._session.scalar(query)

        return self._model_to_entity(model) if model else None

    async def exists(
        self,
        **filters,
    ) -> bool:
        query = select(self.model)

        filter_conditions = self._get_filters(**filters)
        query = query.where(*filter_conditions)
        result = await self._session.scalar(query)

        return result is not None

    async def delete(
        self,
        **filters,
    ) -> int:
        try:
            query = sqlalchemy.delete(self.model)

            filter_conditions = self._get_filters(**filters)
            query = query.where(*filter_conditions)

            result = await self._session.execute(query)
            await self._session.flush()
            return result.rowcount  # type: ignore[attr-defined]
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise DatabaseException from e

    async def count(
        self,
        **filters,
    ) -> int:
        filter_conditions = self._get_filters(**filters)
        return (
            await self._session.scalar(
                select(func.count()).select_from(self.model).where(*filter_conditions)
            )
            or 0
        )

    @staticmethod
    @abstractmethod
    def _model_to_entity(model: SqlAlchemyModel) -> Entity:
        raise NotImplementedError("Subclasses must implement _model_to_entity")

    @staticmethod
    @abstractmethod
    def _entity_to_model(entity: Entity) -> SqlAlchemyModel:
        raise NotImplementedError("Subclasses must implement _entity_to_model")

    @abstractmethod
    def _get_filters(self, **filters) -> List[Any]:
        return []

    @staticmethod
    def _get_order_expression(
        order_by: str, ordering: Ordering
    ) -> sqlalchemy.UnaryExpression[str]:
        if ordering == Ordering.ASC:
            return asc(order_by)
        return desc(order_by)
