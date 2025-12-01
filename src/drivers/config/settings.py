from enum import Enum
from functools import lru_cache

from pydantic_settings import BaseSettings as PydanticBaseSettings


class Environment(str, Enum):
    dev = "development"
    test = "test"
    prod = "production"


class BaseSettings(PydanticBaseSettings):
    app_name: str = "Smart Quote"
    debug: bool = False
    env: Environment = Environment.prod

    db_name: str
    enable_sql_alchemy_logs: bool = False
    cors_url: str = "http://localhost:3000"

    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.db_name}.db"


class DevSettings(BaseSettings):
    debug: bool = True


class TestSettings(BaseSettings):
    debug: bool = True


class ProdSettings(BaseSettings):
    debug: bool = False


settings_mapping: dict[Environment, type[BaseSettings]] = {
    Environment.dev: DevSettings,
    Environment.test: TestSettings,
    Environment.prod: ProdSettings,
}


@lru_cache()
def get_settings():
    config = BaseSettings()
    return settings_mapping[config.env]()
