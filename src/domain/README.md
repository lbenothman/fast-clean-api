# Domain Layer

This document explains the architecture and design patterns of the Domain Layer.

## Overview

The **Domain Layer** is the **innermost layer** containing core business logic and rules. It has **zero external dependencies** - only pure Python.

```
domain/
├── entities/          # Business objects with identity (Task, EntityBase)
├── value_objects/     # Immutable data without identity (CreateTaskData, ListEntity, Ordering)
└── exceptions/        # Business rule violations (TaskNotFound, TaskCannotBeCompleted)
```

## Core Architectural Concepts

### 1. Entities - Business Objects with Identity

**EntityBase** provides common fields inherited by all entities:
- `id`: Unique identifier (UUID)
- `created_at`, `updated_at`: Timestamps

**Task Entity** is our main business object containing:
- **State**: `title`, `description`, `status`, `priority`, `due_date`
- **Behavior**: Methods that encapsulate business logic
- **Rules**: Methods that enforce business constraints

### 2. Rich Domain Model Pattern

Entities are **not just data containers**. They contain behavior and protect their own state.

**State Management**:
```python
# Good: Encapsulated state change
task.mark_as_completed()

# Bad: Direct mutation
task.status = TaskStatus.COMPLETED
```

**Business Rules as Methods**:
- `can_be_completed()` - Guards against completing already completed tasks
- `is_overdue()` - Implements deadline checking logic
- `can_be_deleted()` - Enforces deletion rules

**Why?** Business logic lives in one place, reusable across all use cases, easy to test and maintain.

### 3. Type Safety with Enums

Instead of magic strings, we use enums:

```python
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

**Benefits**:
- Type safety and IDE autocomplete
- Inherits from `str` for easy JSON serialization
- Prevents typos and invalid values

### 4. Value Objects vs Entities

**Entities** (Task):
- Have unique identity (compared by ID)
- Mutable state over time
- Represent things that change

**Value Objects** (CreateTaskData, Ordering):
- No identity (compared by value)
- Immutable after creation
- Represent descriptive data

### 5. Domain Exceptions

Exceptions represent business rule violations:
- `TaskNotFound` - Entity doesn't exist
- `TaskCannotBeCompleted` - Business rule prevents completion
- `TaskCannotBeDeleted` - Business rule prevents deletion

These are **domain concepts**, not technical errors. They're mapped to HTTP status codes in outer layers.

## Architectural Principles

### Dependency Rule: Zero Dependencies

The domain depends on **nothing**:
- ✅ Pure Python (dataclasses, enums, datetime)
- ❌ No FastAPI, SQLAlchemy, or framework imports

**Why?** Business logic should work regardless of web framework, database, or delivery mechanism.

## Integration with Other Layers

**Inward Dependencies Only**:
- **Ports** define interfaces using domain entities
- **Use Cases** orchestrate domain entities
- **Adapters** convert between domain entities and external formats (ORM models)
- **Drivers** convert between domain entities and DTOs (API requests/responses)

All layers depend **inward** toward the domain. The domain depends on nothing.

## Related Documentation

- **[Ports Layer](../ports/README.md)** - Interfaces for domain operations
- **[Use Cases Layer](../use_cases/README.md)** - Domain orchestration
- **[Adapters Layer](../adapters/repositories/README.md)** - Domain persistence
- **[Main README](../README.md)** - Complete architecture overview
