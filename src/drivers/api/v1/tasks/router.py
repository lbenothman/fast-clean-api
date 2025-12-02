from uuid import UUID

from fastapi import APIRouter, Depends, status

from domain.entities.task import Task
from domain.value_objects.create_task_data import CreateTaskData
from drivers.api.v1.tasks.schema import (
    CreateTaskRequest,
    ErrorResponse,
    TaskListParams,
    TaskListResponse,
    TaskResponse,
)
from drivers.dependencies.hateoas import hateoas_dependency
from drivers.dependencies.use_cases import (
    get_complete_task_usecase,
    get_create_task_usecase,
    get_get_all_tasks_usecase,
)
from use_cases.tasks.complete_task_usecase import CompleteTaskUseCase
from use_cases.tasks.create_task_usecase import CreateTaskUseCase
from use_cases.tasks.get_all_tasks_usecase import ListAllTasksUseCase

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
    summary="Create a new task",
    description="Create a new task with the specified title, description, priority, and optional due date.",
)
async def create_task(
    request: CreateTaskRequest,
    create_task_usecase: CreateTaskUseCase = Depends(get_create_task_usecase),
) -> Task:
    data = CreateTaskData(
        title=request.title,
        description=request.description,
        priority=request.priority,
        due_date=request.due_date,
    )
    return await create_task_usecase.execute(data)


@router.get(
    "",
    response_model=TaskListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all tasks",
    description="Retrieve all tasks.",
)
async def list_all_tasks(
    params: TaskListParams = Depends(),
    hateoas=Depends(hateoas_dependency),
    get_all_tasks_usecase: ListAllTasksUseCase = Depends(get_get_all_tasks_usecase),
) -> TaskListResponse:
    result = await get_all_tasks_usecase.execute(
        params=params.model_dump(exclude_none=True, exclude_unset=True)
    )
    return hateoas(items=result.get_items_as_dict(), total_count=result.count)


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        400: {"model": ErrorResponse, "description": "Task cannot be completed"},
    },
    summary="Complete a task",
    description="Mark a task as completed.",
)
async def complete_task(
    task_id: UUID,
    complete_task_usecase: CompleteTaskUseCase = Depends(get_complete_task_usecase),
) -> Task:
    return await complete_task_usecase.execute(task_id=task_id)
