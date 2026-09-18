__all__ = (
    "get_shortener_url_repository",
    "get_user_repository",
    "get_session_token_repository",
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import db_session_getter
from src.repositories.session_repository import SessionTokenRepository
from src.repositories.shortener_url_repository import ShortenerURLRepository
from src.repositories.user_repository import UserRepository


# Depends ShortenerURLRepository
def get_shortener_url_repository(session: AsyncSession = Depends(db_session_getter)) -> ShortenerURLRepository:
    return ShortenerURLRepository(session=session)


def get_user_repository(session: AsyncSession = Depends(db_session_getter)) -> UserRepository:
    return UserRepository(session=session)


def get_session_token_repository(session: AsyncSession = Depends(db_session_getter)) -> SessionTokenRepository:
    return SessionTokenRepository(session=session)
