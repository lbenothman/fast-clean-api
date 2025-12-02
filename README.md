# FastAPI Clean Architecture Template

A comprehensive **FastAPI template tutorial** demonstrating **Clean Architecture** principles through a practical task management system. This project serves as a learning resource and production-ready template for building scalable, maintainable FastAPI applications with proper separation of concerns.

## Table of Contents

- [Overview](#overview)
- [Clean Architecture Principles](#clean-architecture-principles)
- [Project Structure](#project-structure)
- [Architecture Layers](#architecture-layers)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Development Guide](#development-guide)

## Overview

This project implements a task management REST API following **Clean Architecture**. The architecture ensures:

- **Separation of Concerns**: Each layer has a single, well-defined responsibility
- **Independence**: Business logic is independent of frameworks, databases, and external agencies
- **Testability**: Easy to test each layer in isolation
- **Maintainability**: Changes in one layer don't affect others
- **Flexibility**: Easy to swap implementations (e.g., change databases or frameworks)

## Clean Architecture Principles

### The Dependency Rule

Dependencies flow **inward only**:

```
┌─────────────────────────────────────────────────┐
│  Drivers (FastAPI, HTTP)                        │
│  └─ Controllers, Routes, Schemas                │
└─────────────────────────────────────────────────┘
           ↓ depends on
┌─────────────────────────────────────────────────┐
│  Adapters (Infrastructure)                      │
│  └─ Repository Implementations, ORM Models      │
└─────────────────────────────────────────────────┘
           ↓ depends on
┌─────────────────────────────────────────────────┐
│  Use Cases (Application Business Logic)         │
│  └─ CreateTask, CompleteTask, ListTasks         │
└─────────────────────────────────────────────────┘
           ↓ depends on
┌─────────────────────────────────────────────────┐
│  Ports (Interfaces/Contracts)                   │
│  └─ TaskRepositoryInterface (ABC)               │
└─────────────────────────────────────────────────┘
           ↓ depends on
┌─────────────────────────────────────────────────┐
│  Domain (Enterprise Business Rules)             │
│  └─ Task Entity, TaskStatus, Priority           │
└─────────────────────────────────────────────────┘
```

**Key Principle**: Inner layers never depend on outer layers. Outer layers depend on inner layers through abstractions (interfaces).

## Project Structure

```
src/
├── domain/                      # Domain Layer (Core Business Logic)
│   ├── entities/               # Business entities
│   ├── value_objects/          # Value objects (immutable data)
│   └── exceptions/             # Domain-specific exceptions
│   └── README.md               # 📖 Detailed domain documentation
│
├── ports/                      # Ports Layer (Interfaces)
│
├── use_cases/                  # Use Cases Layer (Application Logic)
│
├── adapters/                   # Adapters Layer (Infrastructure)
│   ├── repositories/          # Repository implementations
│   └── connection_engines/    # Database connections
│
├── drivers/                    # Drivers Layer (External Interfaces)
│   ├── api/v1/                # REST API v1
│   ├── config/                # Configuration
│   ├── dependencies/          # Dependency injection
│   ├── exceptions_handlers/   # HTTP exception mapping
│   ├── helpers/               # Helper utilities
│
└── tests/                     # Test Suite
    ├── unit_tests/           # Unit tests
    ├── e2e/                  # End-to-end tests
    └── conftest.py           # Test fixtures
```

## Architecture Layers

### 1. Domain Layer (Innermost)

**Purpose**: Contains enterprise business rules and entities

**Characteristics**:
- Zero external dependencies
- Pure Python dataclasses
- Business logic lives here
- Framework-agnostic

📖 **[Read detailed Domain documentation](src/domain/README.md)**

### 2. Ports Layer (Interfaces)

**Purpose**: Defines contracts/interfaces for external dependencies

**Characteristics**:
- Abstract Base Classes (ABC)
- No implementation details
- Defines what operations are needed, not how

📖 **[Read detailed Ports documentation](src/ports/README.md)**

### 3. Use Cases Layer (Application Business Logic)

**Purpose**: Orchestrates domain entities to fulfill specific application use cases

**Characteristics**:
- Single Responsibility Principle: One use case = one operation
- Depends only on Ports (interfaces) and Domain
- Constructor injection for dependencies
- Single `execute()` method

📖 **[Read detailed Use Cases documentation](src/use_cases/README.md)**

### 4. Adapters Layer (Infrastructure)

**Purpose**: Implements ports/interfaces using specific technologies

**Characteristics**:
- Concrete implementations of repository interfaces
- Handles ORM models and database operations
- Converts between domain entities and persistence models

📖 **[Read detailed Adapters documentation](src/adapters/repositories/README.md)**

### 5. Drivers Layer (External Interfaces)

**Purpose**: Handles external communication (HTTP, CLI, etc.)

**Characteristics**:
- FastAPI routes and controllers
- Request/Response DTOs (Pydantic models)
- Exception handling and HTTP status mapping
- Dependency injection wiring

📖 **[Read detailed Drivers documentation](src/drivers/README.md)**

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI |
| **ASGI Server** | Uvicorn |
| **Database** | SQLite |
| **Async Driver** | aiosqlite |
| **ORM** | SQLAlchemy |
| **Migrations** | Alembic |
| **Validation** | Pydantic |
| **Testing** | pytest + pytest-asyncio |
| **Python** | Python |
| **Package Manager** | uv |

## Getting Started

### Prerequisites

Docker and Docker Compose (recommended)

### Installation with Docker (Recommended)

1. Clone the repository:
```bash
git clone git@github.com:lbenothman/fast-clean-api.git
cd fast-clean-api
```

2. Create a new .env file, based on .env.template and provided the needed values:
```bash
cp .env.template .env
```

3. Build and start the services:
```bash
make build
make upd
```

4. Run database migrations:
```bash
make alembic-db-upgrade
```

5. Access the API:
- API: http://localhost:8000
- Interactive Docs (Swagger): http://localhost:8000/docs
- Alternative Docs (ReDoc): http://localhost:8000/redoc


## Development Guide

### Code Style

```bash
# Format code (inside container)
make format

# Type checking (inside container)
make mypy

# Run pre-commit hooks
make pre-commit
```

### Database Management

#### Alembic Migrations

Common commands (use with `docker exec` or directly):

```bash
# Create a new migration
make alembic-revision

# Apply all pending migrations
make alembic-db-upgrade

# Rollback one migration (inside container)
alembic downgrade -1

# Show current migration version (inside container)
alembic current

# Show migration history (inside container)
alembic history
```

## Contributing

Contributions are welcome! Please follow the existing architecture patterns and ensure all tests pass.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Lotfi Ben Othman
Linkedin: https://www.linkedin.com/in/lotfi-b-17a86681/