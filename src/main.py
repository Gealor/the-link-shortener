from typing import Annotated

import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from schemas.exceptions import InternalDatabaseException
from schemas.pydantic_schemas import BodyCreateSlug
from schemas.pydantic_schemas import URLShort
from services import ShortenerService
from services import get_shortener_service

app = FastAPI()

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
] # адреса, где расположен фронтэнд

app.add_middleware(
    CORSMiddleware, # для корректной работы с фронтэндом
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/short_url")
async def make_short_url(
    url: BodyCreateSlug,
    service: Annotated[ShortenerService, Depends(get_shortener_service)],
) -> URLShort:
    '''
    Make shortener version of URL.
    '''
    try:
        return await service.generate_and_safe_shortcut_url(url.full_url)
    except InternalDatabaseException:
        raise HTTPException(
            status_code=500,
            detail="Error during format url. Please try again."
        ) from None

@app.get("/{code}")
async def redirect(
    code: str,
    service: Annotated[ShortenerService, Depends(get_shortener_service)],
):
    '''
    Return full version url from shortener code
    '''
    return {
        "full_url": "test"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.runtime.host,
        port=settings.runtime.port,
        reload=True,
    )
