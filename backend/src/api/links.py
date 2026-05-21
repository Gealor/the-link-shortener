from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import RedirectResponse

from src.dependencies.rate_limiter_factory import rate_limiter_factory
from src.schemas.exceptions import InternalDatabaseException
from src.schemas.exceptions import OutOfAttemptsForRepeatException
from src.schemas.exceptions import URLBySlugDontExistException
from src.schemas.pydantic_schemas import BodyCreateSlug
from src.schemas.pydantic_schemas import URLShort
from src.services import get_shortener_service
from src.services.shortener_service import ShortenerService

router = APIRouter()

@router.post("/short-url", dependencies=[Depends(rate_limiter_factory(10, 10))])
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

@router.get("/{code}")
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
# разница в том, что при 301 браузер автоматически кеширует ссылку и при переходе на нее повторно уже не будет делаться запрос на бэкенд (не всегда, это зависит от заголовков кэширования)
