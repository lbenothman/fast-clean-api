# Drivers Layer

This document explains the Drivers Layer in Clean Architecture.

## What is the Drivers Layer?

The **Drivers Layer** is the **outermost layer** that handles external interfaces (HTTP, CLI, etc.). It receives requests from the outside world and translates them into operations the application understands.

**Think of it as**: The entry point where external systems interact with your application.

## Core Responsibilities

### 1. HTTP API (FastAPI)

**Routes** define API endpoints:

**Pattern**:
1. Receive HTTP request (DTO)
2. Convert DTO → domain value object
3. Call use case
4. Return domain entity (FastAPI auto-converts to JSON)

### 2. DTOs (Data Transfer Objects)

**Schemas** define API contracts using Pydantic:

**Why DTOs?** Separate API structure from domain structure. API can change without affecting business logic.

### 3. Dependency Injection

**Purpose**: Wire up implementations and inject dependencies into use cases.

**Chain**:
1. Router depends on use case
2. Use case depends on repository
3. FastAPI resolves dependencies automatically

**Benefit**: Loose coupling, easy to swap implementations (e.g., in-memory for tests).

### 4. Exception Mapping

**Purpose**: Convert domain exceptions to HTTP responses.

**Mappings**:
- `TaskNotFound` → 404 Not Found
- `TaskCannotBeCompleted` → 400 Bad Request
- `TaskCannotBeDeleted` → 400 Bad Request
- Domain exceptions stay domain-specific, HTTP details stay here

### 5. Configuration

**Settings** manage environment-based configuration:
- Database connection strings
- CORS settings
- Environment (dev/test/prod)

Uses Pydantic settings for validation and environment variable loading.

## Clean Architecture Position

```
HTTP Request → Router (Drivers) → Use Case → Repository (Adapter) → Domain
            DTO conversion      orchestration    persistence
```

**Dependency Rule**: Drivers depend on everything inward (use cases, domain) but nothing depends on drivers.

## Key Patterns

### DTO Conversion Pattern

**Inbound** (HTTP → Domain):

**Outbound** (Domain → HTTP):

### Dependency Injection Pattern

Three-level injection:
1. **Repository level**: `get_task_repository()` returns concrete repository
2. **Use case level**: `get_create_task_usecase(repository)` injects repository into use case
3. **Router level**: `Depends(get_create_task_usecase)` injects use case into endpoint

### Exception Handling Pattern

Register handlers for each domain exception type:
- Domain throws specific exceptions
- Handlers catch and convert to HTTP responses
- API consumers get proper HTTP status codes

## Benefits

1. **Separation of Concerns**: HTTP details don't leak into business logic
2. **Testability**: Can test use cases without HTTP
3. **Flexibility**: Can add CLI, gRPC, or other interfaces alongside HTTP
4. **API Evolution**: Change API structure without changing domain

## Best Practices

1. **Keep routes thin**: Logic in use cases, not routers
2. **Use DTOs**: Separate API contracts from domain models
3. **Inject dependencies**: Don't instantiate use cases directly
4. **Map exceptions**: Domain exceptions → HTTP status codes
5. **Validate at boundary**: Pydantic validates all input
6. **Version APIs**: `/api/v1/` allows evolution

## Related Documentation

- **[Domain Layer](../domain/README.md)** - Core business logic
- **[Ports Layer](../ports/README.md)** - Interfaces
- **[Use Cases Layer](../use_cases/README.md)** - Application operations
- **[Adapters Layer](../adapters/repositories/README.md)** - Persistence
- **[Main README](../README.md)** - Complete architecture overview
