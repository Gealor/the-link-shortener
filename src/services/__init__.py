__all__ = ("get_shortener_service",)

from fastapi import Depends

from repositories import get_shortener_url_repository
from repositories.shortener_url_repository import ShortenerURLRepository

from .shortener_service import ShortenerService


# Depends ShortenerService
def get_shortener_service(database: ShortenerURLRepository = Depends(get_shortener_url_repository)):
    return ShortenerService(repo=database)
