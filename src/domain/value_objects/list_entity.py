from dataclasses import asdict, dataclass
from typing import Any, Generic, List, TypeVar

from domain.entities.base import EntityBase

T = TypeVar("T", bound=EntityBase)


@dataclass
class ListEntity(Generic[T]):
    items: List[T]
    count: int

    def get_items_as_dict(self) -> List[dict[str, Any]]:
        return [asdict(client) for client in self.items]
