import logging
from pathlib import Path
from pydantic import BaseModel
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
    host: str = '0.0.0.0'
    port: int = 8000

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ENV_TEMPLATE, ENV_FILE),
        case_sensitive=False,
    )

    runtime: RuntimeSettings = RuntimeSettings()
    logger: LogSettings = LogSettings()


settings = Settings()


