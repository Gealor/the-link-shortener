from redis.asyncio import Redis

from core.redis_client import redis_client


def get_redis_client() -> Redis:
    return redis_client
