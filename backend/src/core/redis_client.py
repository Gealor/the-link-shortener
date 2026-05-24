from redis.asyncio import Redis

from .config import settings

redis_client: Redis = Redis(
    host=settings.redis.host,
    port=settings.redis.port,
)

