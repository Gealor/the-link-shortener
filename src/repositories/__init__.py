__all__ = ("get_shortener_url_repository",)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session_getter
from repositories.shortener_url_repository import ShortenerURLRepository


# Depends ShortenerURLRepository
def get_shortener_url_repository(session: AsyncSession = Depends(db_session_getter)) -> ShortenerURLRepository:
    return ShortenerURLRepository(session=session)
