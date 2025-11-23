from pydantic import BaseModel, ConfigDict, Field, computed_field
from core.config import settings


class URLShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_url: str = Field(examples=["https://google.com/?something=2345676812"])
    slug: str = Field(examples=["9DwYb3"])

    @computed_field
    def full_slug(self) -> str:
        return f"{settings.runtime.protocol}://{settings.runtime.host}:{settings.runtime.port}/{self.slug}"