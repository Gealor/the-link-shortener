import logging
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

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
    host: str = '0.0.0.0'
    port: int = 8000

class FullSlugURLSettings(RuntimeSettings):
    protocol: str = "http"
    host: str = "localhost"

class DatabaseSettings(BaseModel):
    db_name: Annotated[str, Field(alias="POSTGRES_DB")]
    db_user: Annotated[str, Field(alias="POSTGRES_USER")]
    db_password: Annotated[str, Field(alias="POSTGRES_PASSWORD")]
    db_host: str = "localhost"
    db_echo: bool = False

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:6000/{self.db_name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ENV_TEMPLATE, ENV_FILE),
        case_sensitive=False, # чувствительность к регистру
        env_nested_delimiter="__", # обязательный параметр, если настройки поделены на разные классы,
    # в этом случае в .env у параметров указывается сначала имя переменной, в которой лежат переменные в python коде,
    # потом уже этот разделитель __ и после этого уже имя переменной окружения,
    # т.е. если мы в главном классе настроек Settings создали атрибут database,
    # то в .env переменные окружения должны начинаться с DATABASE__(либо database__, если у нас case_sensitive=True)
    )

    runtime: RuntimeSettings = RuntimeSettings()
    full_slug: FullSlugURLSettings = FullSlugURLSettings()
    logger: LogSettings = LogSettings()
    database: DatabaseSettings

    count_repeating: int = 3

settings = Settings()


