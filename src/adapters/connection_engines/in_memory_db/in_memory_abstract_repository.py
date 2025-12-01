from abc import ABC, abstractmethod
from operator import attrgetter
from typing import Dict, Generic, List, TypeVar
from uuid import UUID, uuid4

from domain.entities.base import EntityBase
from domain.value_objects.ordering import Ordering

T = TypeVar("T", bound=EntityBase)


class InMemoryAbstractRepository(ABC, Generic[T]):
    def __init__(self) -> None:
        # A dictionary to store entities in-memory, using UUID as the key
        self._storage: Dict[UUID, T] = {}

    async def save(self, entity: T) -> T:
        """
        Save an entity in-memory.
        """

        entity.id = uuid4()
        self._storage[entity.id] = entity
        return entity

    async def get(self, **filters) -> T | None:
        """
        Get an entity by filters.
        Returns None if the entity is not found.
        """
        for entity in self._storage.values():
            if self._get_filters(entity, **filters):
                return entity
        return None

    async def update(self, fields_to_update: dict, **filters) -> int:
        """
        Update entities matching the filters with the provided fields.
        Returns the number of entities updated.
        """
        updated_count = 0
        for entity in self._storage.values():
            if self._get_filters(entity, **filters):
                for field, value in fields_to_update.items():
                    if hasattr(entity, field):
                        setattr(entity, field, value)
                updated_count += 1
        return updated_count

    def delete(self, key: UUID) -> None:
        """
        Delete an entity by its UUID.
        Throws KeyError if the entity is not found.
        """
        if key not in self._storage:
            raise KeyError(f"Entity with UUID {key} not found.")
        del self._storage[key]

    async def list_all(
        self,
        page: int = 1,
        limit: int = 10,
        order_by: str = "created_at",
        ordering: Ordering = Ordering.ASC,
        **filters,
    ) -> List[T]:
        filtered_entities = [
            entity
            for entity in self._storage.values()
            if self._get_filters(entity, **filters)
        ]

        if ordering == Ordering.ASC:
            sorted_entities = sorted(filtered_entities, key=attrgetter(order_by))
        else:
            sorted_entities = sorted(
                filtered_entities, key=attrgetter(order_by), reverse=True
            )

        start = (page - 1) * limit
        end = start + limit
        return sorted_entities[start:end]

    async def count(
        self,
        **filters,
    ) -> int:
        filtered_entities = [
            entity
            for entity in self._storage.values()
            if self._get_filters(entity, **filters)
        ]

        return len(filtered_entities)

    @abstractmethod
    def _get_filters(self, entity: T, **filters) -> bool:
        pass
