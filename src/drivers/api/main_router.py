from typing import Annotated

from fastapi import APIRouter, Depends

from drivers.config.settings import BaseSettings, get_settings

router = APIRouter()


@router.get("/")
async def home(settings: Annotated[BaseSettings, Depends(get_settings)]):
    return {"message": f"Hello from {settings.app_name}"}
