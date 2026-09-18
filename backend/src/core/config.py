import logging
from pathlib import Path
from typing import Annotated
from typing import Literal

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

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ENV_TEMPLATE, ENV_FILE),
        case_sensitive=False,
        extra="ignore", # Игнорировать другие переменные в .env
    )

    db_name: Annotated[str, Field(alias="POSTGRES_DB")]
    db_user: Annotated[str, Field(alias="POSTGRES_USER")]
    db_password: Annotated[str, Field(alias="POSTGRES_PASSWORD")]
    db_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    db_port: int = Field(default=6000, alias="POSTGRES_PORT")
    db_echo: bool = False

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ENV_TEMPLATE, ENV_FILE),
        case_sensitive=False,
        extra="ignore", # Игнорировать другие переменные в .env
    )

    host: Annotated[str, Field(alias="REDIS_HOST")]
    port: Annotated[int, Field(alias="REDIS_PORT")]

class AuthSettings(BaseModel):
    session_id_cookie_name: str = "session_id"
    session_id_expire_days: int = 7
    http_only: bool = True
    session_cookie_secure: bool = False  # True в проде (HTTPS)
    samesite: Literal["strict", "lax", "none"] = "lax"

    @property
    def session_id_expire_minutes(self) -> int:
        return 24 * 60 * self.session_id_expire_days

    @property
    def session_id_expire_seconds(self) -> int:
        return self.session_id_expire_minutes * 60


class RateLimitSettings(BaseModel):
    topic_name: str = "rate_limiter"
    window_size: int = 10
    ttl_seconds: int = window_size*2


class CsrfSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ENV_TEMPLATE, ENV_FILE),
        case_sensitive=False,
        extra="ignore", # Игнорировать другие переменные в .env
    )

    secret_key: Annotated[str, Field(alias="CSRF_SECRET_KEY")]
    cookie_samesite: Literal["none", "lax", "strict"] = "lax"
    cookie_secure: bool = False
    httponly: bool = True
    token_location: Literal["body", "header", "both"] = "header"
    token_key: str = "X-CSRF-Token"
    # CSRF-кука не должна протухать раньше сессии (токен стабилен на всю сессию,
    # а не ротируется на каждый запрос) — иначе живой session_id, но 403 на CSRF.
    max_age: int = Field(default_factory=lambda: AuthSettings().session_id_expire_seconds)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ENV_TEMPLATE, ENV_FILE),
        case_sensitive=False, # чувствительность к регистру
        env_nested_delimiter="__", # обязательный параметр, если настройки поделены на разные классы,
    # в этом случае в .env у параметров указывается сначала имя переменной, в которой лежат переменные в python коде,
    # потом уже этот разделитель __ и после этого уже имя переменной окружения,
    # т.е. если мы в главном классе настроек Settings создали атрибут database,
    # то в .env переменные окружения должны начинаться с DATABASE__(либо database__, если у нас case_sensitive=True)
        extra="ignore",
    )

    runtime: RuntimeSettings = RuntimeSettings()
    full_slug: FullSlugURLSettings = FullSlugURLSettings()
    logger: LogSettings = LogSettings()
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)  # type: ignore[arg-type]
    redis: RedisSettings = Field(default_factory=RedisSettings)  # type: ignore[arg-type]
    rate_limiter: RateLimitSettings = RateLimitSettings()
    auth: AuthSettings = AuthSettings()
    csrf: CsrfSettings = Field(default_factory=CsrfSettings)  # type: ignore[arg-type]

    count_repeating: int = 3
    backoff_factor: int = 2

settings = Settings()


