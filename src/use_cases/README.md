# Use Cases Layer

This document explains the Use Cases Layer in Clean Architecture.

## What is a Use Case?

A **Use Case** is a single application operation that orchestrates domain entities to fulfill a specific business goal.

**Examples**: CreateTask, CompleteTask, GetAllTasks

## Use Case Pattern

Every use case follows the same structure:

**Pattern Elements**:
1. **Constructor injection**: Dependencies injected via `__init__`
2. **Single execute method**: One public method per use case
3. **Orchestration**: Coordinates domain entities and repositories
4. **No business logic**: Delegates to domain entities

## Key Principles

### 1. Single Responsibility

One use case = one operation:
- `CreateTaskUseCase` - Creates a task
- `CompleteTaskUseCase` - Marks task as completed
- `GetAllTasksUseCase` - Lists tasks with filters

**Not**: `TaskUseCase` with multiple operations.

### 2. Dependency Injection

Use cases depend on **interfaces** (ports), not concrete implementations:
This allows testing with in-memory implementations.

### 3. Orchestration, Not Logic

Use cases **coordinate** but don't contain business rules:
Business rules live in domain entities, use cases just orchestrate.

### 4. Application Flow

Typical use case flow:
1. Receive input (from driver layer)
2. Retrieve entities (via repository)
3. Validate (check business rules)
4. Execute domain logic (call entity methods)
5. Persist changes (via repository)
6. Return result

## Clean Architecture Position

```
Drivers (API) → Use Cases → Ports (interfaces) → Domain (entities)
                    ↓ orchestrates
                  Domain entities
```

**Dependencies**:
- Use cases depend on ports (interfaces)
- Use cases depend on domain (entities)
- Use cases **don't** depend on adapters or drivers

## Best Practices

1. **One class per use case**: Single responsibility
2. **Constructor injection**: Dependencies via `__init__`
3. **Single execute method**: One public method
4. **Depend on interfaces**: Use ports, not adapters
5. **Delegate to domain**: Business logic in entities
6. **Explicit exceptions**: Raise domain exceptions for errors

## Related Documentation

- **[Domain Layer](../domain/README.md)** - Entities orchestrated by use cases
- **[Ports Layer](../ports/README.md)** - Interfaces used by use cases
- **[Adapters Layer](../adapters/repositories/README.md)** - Repository implementations
- **[Drivers Layer](../drivers/README.md)** - API layer that calls use cases
- **[Main README](../../README.md)** - Complete architecture overview
