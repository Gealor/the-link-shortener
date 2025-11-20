from pydantic import BaseModel, ConfigDict, Field


class URLShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_url: str = Field(examples=["https://google.com/?something=2345676812"])
    slug: str = Field(examples=["9DwYb3"])