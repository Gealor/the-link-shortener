from fastapi import Request
from fastapi import Response

from src.core.config import settings
from src.core.logger import log


def set_session_cookie(key: str, value: str, response: Response) -> None:
    log.info("Setup cookie %s...", key)
    response.set_cookie(
        key=key,
        value=value,
        httponly=settings.auth.http_only,
        secure=settings.auth.session_cookie_secure,
        samesite=settings.auth.samesite,
        max_age=settings.auth.session_id_expire_minutes * 60,
        path="/",
    )


def clear_session_cookie(key: str, response: Response) -> None:
    log.info("Delete cookie %s...", key)
    response.delete_cookie(
        key=key,
        samesite=settings.auth.samesite,
        secure=settings.auth.session_cookie_secure,
        path="/",
    )


def get_value_from_cookie(key: str, request: Request) -> str | None:
    return request.cookies.get(key, None)
