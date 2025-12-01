from dataclasses import dataclass, asdict
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass
class ListEntity(Generic[T]):
    items: List[T]
    count: int

    def get_items_as_dict(self) -> List[T]:
        return [asdict(client) for client in self.items]