from typing import Annotated

import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from core.config import settings
from schemas.exceptions import InternalDatabaseException
from schemas.exceptions import OutOfAttemptsForRepeatException
from schemas.exceptions import URLBySlugDontExistException
from schemas.pydantic_schemas import BodyCreateSlug
from schemas.pydantic_schemas import URLShort
from services import ShortenerService
from services import get_shortener_service

app = FastAPI(
    title="Link Shortener",
    description="This is pet-project Link Shortener"
)

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
    """
    Make shortener version of URL.

    Args:
        url (BodyCreateSlug): full url in http format to get slug

    Raises:
        HTTPException: 400, Error during format url. Please try again.

    Returns:
        URLShort: Contain slug, full_slug and original url
    """

    try:
        return await service.generate_and_safe_shortcut_url(url.full_url)
    except OutOfAttemptsForRepeatException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate slug. Please try again."
        ) from exc
    except InternalDatabaseException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error during format url. Please try again."
        ) from exc

@app.get("/{code}")
async def redirect(
    code: str,
    service: Annotated[ShortenerService, Depends(get_shortener_service)],
):
    """
    Redirect to full version url from shortener code

    Args:
        code (str): identificator in shortener url to get original URL

    Returns:
        RedirectResponse: redirects to original full url
    """
    try:
        result = await service.get_full_url_by_slug(code=code)
    except URLBySlugDontExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        ) from exc
    return RedirectResponse(
        url=str(result.full_url),
        status_code=status.HTTP_302_FOUND,
    ) # для редиректов используются коды ответов 301 либо 302,
# разница в том, что при 301 браузер автоматически кеширует ссылку и при переходе на нее повторно уже не будет делаться запрос на бэкенд


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.runtime.host,
        port=settings.runtime.port,
        reload=True,
    )
