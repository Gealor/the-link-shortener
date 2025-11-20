from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR / '.env'
ENV_TEMPLATE = BASE_DIR / '.env.template'

class RuntimeSettings(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ENV_TEMPLATE, ENV_FILE),
        case_sensitive=False,
    )

    runtime: RuntimeSettings = RuntimeSettings()


settings = Settings()


