__all__ = ("get_shortener_service", "get_auth_service")

from fastapi import Depends

from src.repositories import get_session_token_repository
from src.repositories import get_shortener_url_repository
from src.repositories import get_user_repository
from src.repositories.session_repository import SessionTokenRepository
from src.repositories.shortener_url_repository import ShortenerURLRepository
from src.repositories.user_repository import UserRepository

from .auth_service import AuthService
from .shortener_service import ShortenerService


# Depends ShortenerService
def get_shortener_service(database: ShortenerURLRepository = Depends(get_shortener_url_repository)):
    return ShortenerService(repo=database)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    token_repo: SessionTokenRepository = Depends(get_session_token_repository),
) -> AuthService:
    return AuthService(user_repo=user_repo, token_repo=token_repo)
