from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID


@dataclass(kw_only=True)
class EntityBase:
    id: UUID | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
