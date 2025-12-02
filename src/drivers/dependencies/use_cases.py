from fastapi import Depends

from drivers.dependencies.repositories import get_task_repository
from ports.task_repository_interface import TaskRepositoryInterface
from use_cases.tasks.complete_task_usecase import CompleteTaskUseCase
from use_cases.tasks.create_task_usecase import CreateTaskUseCase
from use_cases.tasks.get_all_tasks_usecase import ListAllTasksUseCase


def get_create_task_usecase(
    repository: TaskRepositoryInterface = Depends(get_task_repository),
) -> CreateTaskUseCase:
    return CreateTaskUseCase(repository)


def get_complete_task_usecase(
    repository: TaskRepositoryInterface = Depends(get_task_repository),
) -> CompleteTaskUseCase:
    return CompleteTaskUseCase(repository)


def get_get_all_tasks_usecase(
    repository: TaskRepositoryInterface = Depends(get_task_repository),
) -> ListAllTasksUseCase:
    return ListAllTasksUseCase(repository)
