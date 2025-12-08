__all__ = ("ShortenerService")

from fastapi import Depends

from core.database import db_session_getter
from .shortener_service import ShortenerService

from sqlalchemy.ext.asyncio import AsyncSession

# Depends ShortenerService
def get_shortener_service(session: AsyncSession = Depends(db_session_getter)):
    return ShortenerService(session=session)