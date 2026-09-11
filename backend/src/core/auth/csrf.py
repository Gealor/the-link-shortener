from typing import Annotated

from fastapi import Depends
from fastapi import Request
from fastapi import Response
from fastapi_csrf_protect import CsrfProtect

from src.core.config import settings

CSRF_Secure = Annotated[CsrfProtect, Depends()]

CSRF_ERROR_HEADER = "X-CSRF-Error"

@CsrfProtect.load_config
def get_csrf_config():
  return settings.csrf


def issue_csrf_token(csrf_protect: CSRF_Secure, response: Response) -> str:
    raw_token, signed_token = csrf_protect.generate_csrf_tokens()
    csrf_protect.set_csrf_cookie(signed_token, response)
    return raw_token


def set_csrf_cache_headers(response: Response) -> None:
    response.headers["Cache-Control"] = f"private, max-age={settings.csrf.max_age}"
    response.headers["Vary"] = "Cookie" # Vary - заголовок, который определяет, какие заголовки нужно учитывать при формировании ключа кэша.
    # в данном случае на основе Cookie, т.е. каждая уникальная кука создает отдельную запись в кеше - неэффективно


async def verify_csrf(request: Request, csrf_protect: CSRF_Secure) -> None:
    await csrf_protect.validate_csrf(request=request)
