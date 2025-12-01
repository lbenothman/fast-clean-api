from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID


@dataclass(kw_only=True)
class EntityBase:
    id: UUID | None = None
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
