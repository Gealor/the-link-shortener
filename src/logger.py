import logging

from core.config import settings

logging.basicConfig(
    format=settings.logger.LOG_DEFAULT_FORMAT,
    datefmt=settings.logger.datefmt,
    level=settings.logger.level,
)

log = logging.getLogger(__name__)

