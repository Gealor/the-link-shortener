__all__ = ("get_shortener_service",)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session_getter

from .shortener_service import ShortenerService


# Depends ShortenerService
def get_shortener_service(session: AsyncSession = Depends(db_session_getter)):
    return ShortenerService(session=session)
