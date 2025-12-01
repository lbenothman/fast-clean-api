# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI-based task management system following Clean Architecture principles with strict separation of concerns. This project serves as a tutorial for building FastAPI applications with Clean Architecture.

## Architecture

This project follows **Clean Architecture** with dependencies pointing inward:

```
Domain ← Ports ← UseCases ← Drivers
```

Inner layers have no knowledge of outer layers. All external dependencies are abstracted behind port interfaces (ABCs).

## Project Structure

```
src/
├── domain/              # Enterprise business rules (zero dependencies)
│   ├── entities/        # Pure dataclasses (Task with TaskStatus/Priority enums)
│   └── exceptions/      # Domain-specific exceptions
│
├── ports/               # Abstract interfaces (ABC)
│   └── *_interface.py   # Repository contracts
│
├── use_cases/           # Application business logic
│   └── tasks/           # Single-responsibility operations
│
├── adapters/            # Interface adapters
│   ├── repositories/    # Repository implementations
│   └── connection_engines/  # Database connection & models
│
└── drivers/             # Frameworks & drivers (FastAPI layer)
    ├── api/v1/
    │   └── tasks/       # Task endpoints (routes & schemas)
    ├── config/          # Environment-based settings
    ├── dependencies/    # Dependency injection wiring
    └── exceptions_handlers/ # HTTP exception mapping
```

## Tech Stack

- **Framework**: FastAPI 0.122.0
- **ASGI Server**: Uvicorn 0.37.0
- **Database**: SQLite (via aiosqlite)
- **ORM**: SQLAlchemy 2.0.44 (async)
- **Validation**: Pydantic v2 (via pydantic-settings 2.8.0)
- **Migration**: Alembic 1.17.0
- **Python**: >=3.12
- **Package Manager**: uv (evidenced by uv.lock)

## Running the Application

```bash
# Install dependencies
uv sync

# Run database migrations
alembic upgrade head

# Run development server
uvicorn drivers.main:app --reload

# Or with specific host/port
uvicorn drivers.main:app --host 0.0.0.0 --port 8000
```

## Development Tools

```bash
# Install dev dependencies
uv sync --extra dev

# Run type checking
mypy src/

# Format code
black src/
isort src/

# Lint
ruff check src/

# Run tests (pytest configured for async)
pytest
```

## Key Architectural Patterns

### Ports (Interfaces)

All external dependencies are abstracted behind ABC interfaces in `ports/`:

```python
# ports/task_repository_interface.py
class TaskRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, task: Task) -> Task: ...

    @abstractmethod
    async def get_by_id(self, task_id: UUID) -> Task | None: ...

    @abstractmethod
    async def get_all(self) -> list[Task]: ...

    @abstractmethod
    async def update(self, task: Task) -> Task: ...

    @abstractmethod
    async def delete(self, task_id: UUID) -> None: ...
```

### Use Cases

Each use case is a single class with constructor injection and an `execute` method:

```python
class CompleteTaskUseCase:
    def __init__(self, repository: TaskRepositoryInterface):
        self.repository = repository

    async def execute(self, task_id: UUID) -> Task:
        task = await self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFound(str(task_id))

        if not task.can_be_completed():
            raise TaskCannotBeCompleted(str(task_id))

        task.mark_as_completed()
        return await self.repository.update(task)
```

### Domain Entities

Pure Python dataclasses with no framework dependencies and business logic methods:

```python
@dataclass
class Task:
    title: str
    description: str
    status: TaskStatus
    priority: Priority
    id: UUID | None = None
    due_date: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def mark_as_completed(self) -> None:
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED

    def is_overdue(self) -> bool:
        """Check if the task is overdue."""
        if self.due_date is None:
            return False
        return datetime.now() > self.due_date and self.status != TaskStatus.COMPLETED

    def can_be_completed(self) -> bool:
        """Check if the task can be marked as completed."""
        return self.status != TaskStatus.COMPLETED
```

### Enums

Domain enums are defined as string enums for easy serialization:

```python
class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

### Exception Handling

Domain exceptions are mapped to HTTP responses in `drivers/exceptions_handlers/handlers.py`:

- `EntityNotFound` → 404
- `TaskNotFound` (inherits from EntityNotFound) → 404
- `TaskCannotBeCompleted` → 400
- `TaskCannotBeDeleted` → 400
- `EntityAlreadyExists` → 409
- `InvalidEntityReference` → 422
- `RequestValidationError` → 422

Custom exceptions inherit from base domain exceptions (e.g., `TaskNotFound(EntityNotFound)`).

### Configuration

Environment-based settings using Pydantic:

- `BaseSettings` loads from environment variables
- Environment determined by `env` field (dev/test/prod)
- Settings accessed via `get_settings()` (cached with `@lru_cache`)
- Required fields: `db_name`, `cors_url`
- Database URL: `sqlite+aiosqlite:///{db_name}.db`

## API Endpoints

Currently implemented:

| Method | Route                          | Description                           |
|--------|--------------------------------|---------------------------------------|
| GET    | `/`                            | Health check / home                   |
| POST   | `/api/v1/tasks`                | Create a new task                     |
| GET    | `/api/v1/tasks`                | Get all tasks                         |
| PATCH  | `/api/v1/tasks/{task_id}`      | Update a task                         |
| PATCH  | `/api/v1/tasks/{task_id}/complete` | Mark a task as completed          |
| DELETE | `/api/v1/tasks/{task_id}`      | Delete a task                         |

## Import Conventions

- Use absolute imports from `src/`: `from domain.entities.task import Task`
- Sometimes prefixed: `from src.domain.entities.task import Task`
- No relative imports

## Code Conventions

- **Type hints**: Required everywhere, use `| None` not `Optional`
- **Async**: All I/O operations must be async
- **Entities**: Pure dataclasses, no framework dependencies
- **Enums**: String enums for easy serialization (inherit from `str` and `Enum`)
- **Repositories**: Return domain entities, not ORM models
- **Use Cases**: Inject ports via constructor, single public `execute` method
- **DTOs**: Pydantic models in `drivers/api/v1/*/schemas.py` for API contracts
- **Domain Logic**: Business rules live in entity methods (e.g., `can_be_completed()`, `is_overdue()`)

## Repository Pattern

Repositories handle conversion between domain entities and ORM models:

```python
# In repository save method
task_model = TaskModel(
    id=str(task.id),
    title=task.title,
    status=task.status.value,  # Convert enum to string
    priority=task.priority.value,
    # ... other fields
)

# In repository _to_entity method
return Task(
    id=UUID(task_model.id),
    title=task_model.title,
    status=TaskStatus(task_model.status),  # Convert string to enum
    priority=Priority(task_model.priority),
    # ... other fields
)
```

## Dependency Injection

Use cases receive repository implementations via FastAPI's dependency injection:

```python
# In drivers/dependencies/use_cases.py
def get_create_task_usecase(
    repository: TaskRepositoryInterface = Depends(get_task_repository),
) -> CreateTaskUseCase:
    return CreateTaskUseCase(repository)

# In route handler
async def create_task(
    request: CreateTaskRequest,
    create_task_usecase: CreateTaskUseCase = Depends(get_create_task_usecase),
) -> TaskResponse:
    # Use the injected use case
    task = await create_task_usecase.execute(...)
```

## Testing Configuration

pytest configured in `pyproject.toml`:
- `asyncio_mode = "auto"` - automatically handles async tests
- `asyncio_default_fixture_loop_scope = "session"` - shared event loop for all fixtures

## Tutorial Notes

This project is designed as a tutorial for FastAPI with Clean Architecture:

- **Simple Domain**: Tasks are easy to understand (no external dependencies like customer_id or product_id)
- **Complete CRUD**: Demonstrates all basic operations (Create, Read, Update, Delete)
- **Business Logic**: Shows domain logic in entity methods
- **Separation of Concerns**: Clear boundaries between layers
- **Type Safety**: Full type hints with enums instead of magic strings
- **Database**: SQLite for easy setup (via aiosqlite)
- **Async**: Demonstrates async/await patterns throughout

## Database

- **Type**: SQLite (development-friendly)
- **Driver**: aiosqlite (async SQLite driver)
- **Migrations**: Alembic for schema versioning
- **Models**: SQLAlchemy 2.0 with modern Mapped[] syntax

## Instructions
- For each new question/request display a welcome message with my name, my name is Lotfi
- Never add comments or docstrings
- Always use fixture instead of creating new instances of objects or entities for the tests
- Always use existing fixtures for the tests, you can add new if needed
