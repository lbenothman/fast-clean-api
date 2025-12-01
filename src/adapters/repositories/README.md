# Adapters Layer - Repositories

This document explains the Adapters Layer and Repository implementations.

## What is an Adapter?

An **Adapter** is a concrete implementation of a port (interface) that connects the application to external systems (databases, APIs, services, etc.).

**Analogy**: If a port is a plug socket, an adapter is the specific device you plug in.

## Multiple Implementations

We could provide multiple repository implementations for the same interface:

### 1. SqlAlchemyTaskRepository (Production)

**Purpose**: Persist tasks in a real database (SQLite, PostgreSQL)

**Key Responsibilities**:
- Convert domain entities ↔ ORM models
- Build database queries with filters
- Handle database transactions

**Inherits from**: `SqlAlchemyAbstractRepository` (provides CRUD operations)

### 2. InMemoryTaskRepository (Testing)

**Purpose**: Store tasks in memory for fast testing without database

**Key Responsibilities**:
- Store entities in a dictionary
- Filter entities in memory
- No database connection needed

**Inherits from**: `InMemoryAbstractRepository` (provides in-memory storage)

## Adapter Responsibilities

### 1. Implement Port Interface

Adapters must implement all methods from `TaskRepositoryInterface`:
- `save()`, `get()`, `list_all()`, `count()`, `update()`, `delete()`

### 2. Handle Technology-Specific Details

**SqlAlchemyRepository**:
- Database sessions
- SQL query building
- Transaction management
- ORM model mapping

**InMemoryRepository**:
- Dictionary storage
- In-memory filtering
- No persistence

## Clean Architecture Position

```
Use Cases → depend on → TaskRepositoryInterface (Port)
                              ↑ implements
                     SqlAlchemyRepository (Adapter)
                              ↓ uses
                          TaskModel (ORM)
                              ↓ persists to
                          Database
```

**Dependency direction**: Adapter depends on port, not the reverse.

## Best Practices

1. **Implement interface completely**: All port methods must be implemented
2. **Convert at boundaries**: Domain entities in/out, infrastructure types internal
3. **Handle errors**: Database errors → domain exceptions
4. **No business logic**: Adapters are for translation and persistence only
5. **Technology-specific code stays here**: SQL queries, ORM config, etc.

## Related Documentation

- **[Domain Layer](../../domain/README.md)** - Entities stored by repositories
- **[Ports Layer](../../ports/README.md)** - Interfaces implemented by adapters
- **[Use Cases Layer](../../use_cases/README.md)** - Consumers of repositories
- **[Main README](../../README.md)** - Complete architecture overview
