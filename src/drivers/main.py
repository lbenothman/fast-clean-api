import logging.config
import pathlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from drivers.api.main_router import router as main_router
from drivers.api.v1.tasks.router import router as tasks_router
from drivers.config.settings import get_settings
from drivers.exceptions_handlers.handlers import add_handlers


def create_app() -> FastAPI:
    application = FastAPI(title="Clean Architecture FastAPI")

    settings = get_settings()

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.cors_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(main_router)
    application.include_router(tasks_router)
    add_handlers(application)

    parent_folder = pathlib.Path(__file__).parent.parent.resolve()
    logging.config.fileConfig(
        f"{parent_folder}/logging.ini", disable_existing_loggers=False
    )
    return application


app = create_app()
