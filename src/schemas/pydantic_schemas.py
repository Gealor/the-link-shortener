from pydantic import BaseModel, ConfigDict, Field, HttpUrl, computed_field
from core.config import settings

class BaseURL(BaseModel):
    full_url: HttpUrl = Field(examples=["https://google.com/?something=2345676812"])

class BodyCreateSlug(BaseURL):
    pass

class URLShort(BaseURL):
    model_config = ConfigDict(from_attributes=True)
    
    slug: str = Field(examples=["9DwYb3"])

    @computed_field
    def full_slug(self) -> str:
        return f"{settings.full_slug.protocol}://{settings.full_slug.host}:{settings.runtime.port}/{self.slug}"



class CreateShortURL(BaseModel):
    full_url: str = Field(examples=["https://google.com/?something=2345676812"])
    slug: str = Field(examples=["9DwYb3"])