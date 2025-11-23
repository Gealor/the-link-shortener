import logging
from pathlib import Path
from typing import Annotated
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR / '.env'
ENV_TEMPLATE = BASE_DIR / '.env.template'

class LogSettings(BaseModel):
    LOG_DEFAULT_FORMAT: str = (
        "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    )
    level: int = logging.INFO
    datefmt: str = "%Y-%m-%d %H:%M:%S"

class RuntimeSettings(BaseModel):
    protocol: str = "http"
    host: str = '0.0.0.0'
    port: int = 8000

class DatabaseSettings(BaseModel):
    db_name: Annotated[str, Field(alias="POSTGRES_DB")]
    db_user: Annotated[str, Field(alias="POSTGRES_USER")]
    db_password: Annotated[str, Field(alias="POSTGRES_PASSWORD")]
    db_host: str = "localhost"

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:6000/{self.db_name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ENV_TEMPLATE, ENV_FILE),
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    runtime: RuntimeSettings = RuntimeSettings()
    logger: LogSettings = LogSettings()
    database: DatabaseSettings

settings = Settings()


