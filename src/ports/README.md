# Ports Layer

This document explains the Ports Layer in Clean Architecture.

## What is a Port?

A **Port** is an **abstract interface** (contract) that defines operations needed by business logic without specifying how they're implemented.

Think of it as a **plug socket**: the socket defines the interface, but you can plug in different devices (implementations).

## Core Concept: Dependency Inversion

**Without Ports** (Bad):
```
Use Cases → depend on → SqlAlchemyRepository (concrete implementation)
```
Problem: Tightly coupled to specific database technology.

**With Ports** (Good):
```
Use Cases → depend on → TaskRepositoryInterface (abstract)
                              ↑ implements
                    SqlAlchemyRepository / InMemoryRepository
```
Solution: Business logic depends on abstraction, not implementation.

**Key Points**:
- Abstract Base Class (ABC)
- Uses domain entities (Task), not database models
- No implementation - just method signatures
- Multiple implementations possible (SQL, NoSQL, In-Memory)

## Clean Architecture Structure

```
Domain (entities)
    ↑
Ports (interfaces) ← Use Cases depend on this
    ↑
Adapters (implementations) ← Outer layer implements this
```

**Dependency Rule**: Inner layers define interfaces, outer layers implement them.

## Benefits

1. **Testability**: Use in-memory implementation for tests, no database needed
2. **Flexibility**: Swap implementations (SQLite → PostgreSQL) without changing use cases
3. **Independence**: Business logic doesn't know about databases or frameworks

## Related Documentation

- **[Domain Layer](../domain/README.md)** - Entities used in port signatures
- **[Use Cases Layer](../use_cases/README.md)** - Consumers of ports
- **[Adapters Layer](../adapters/repositories/README.md)** - Port implementations
- **[Main README](../README.md)** - Complete architecture overview
