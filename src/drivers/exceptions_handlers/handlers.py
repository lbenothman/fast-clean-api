from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from domain.exceptions.common import (
    EntityAlreadyExists,
    EntityNotFound,
    InvalidEntityReference,
)
from domain.exceptions.task_exception import TaskCannotBeCompleted, TaskCannotBeDeleted, TaskUpdateFailed


def add_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        RequestValidationError, pydantic_validation_exception_handler
    )
    app.add_exception_handler(EntityAlreadyExists, http_409_exception_handler)
    app.add_exception_handler(EntityNotFound, http_404_exception_handler)
    app.add_exception_handler(InvalidEntityReference, http_422_exception_handler)
    app.add_exception_handler(TaskCannotBeCompleted, http_400_exception_handler)
    app.add_exception_handler(TaskCannotBeDeleted, http_400_exception_handler)
    app.add_exception_handler(TaskUpdateFailed, http_409_exception_handler)


async def pydantic_validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),  # type: ignore
    )


async def http_409_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content=jsonable_encoder({"detail": str(exc)}),
    )


async def http_404_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content=jsonable_encoder({"detail": str(exc)}),
    )


async def http_422_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": str(exc)}),
    )


async def http_401_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content=jsonable_encoder({"detail": str(exc)}),
    )


async def http_400_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": str(exc)}),
    )


async def http_413_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=413,
        content=jsonable_encoder({"detail": str(exc)}),
    )


async def http_500_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"detail": str(exc)}),
    )
