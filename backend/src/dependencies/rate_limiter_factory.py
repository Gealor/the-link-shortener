from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from redis.asyncio import Redis

from core.config import settings
from core.logger import log
from src.core.rate_limiters import RateLimiterProtocol
from src.core.rate_limiters import RateLimiterSlidingWindowCounter
from src.core.rate_limiters import RateLimiterSlidingWindowLog
from src.dependencies.redis_client import get_redis_client


def get_rate_limiter(
    redis: Redis = Depends(get_redis_client)
) -> RateLimiterProtocol:
    return RateLimiterSlidingWindowCounter(redis)


def rate_limiter_factory(
    max_requests: int,
    window_seconds: int = settings.rate_limiter.window_size,
):
    async def dependency(
        request: Request,
        rate_limiter: RateLimiterProtocol = Depends(get_rate_limiter)
    ):
        endpoint = request.url.path
        ip_address = request.client.host
        log.info("IP address: %s", ip_address)
        log.info("Enpoint: %s", endpoint)

        limited = await rate_limiter.is_limited(
            ip_address=ip_address,
            endpoint=endpoint,
            max_requests=max_requests,
            window_seconds=window_seconds,
        )
        log.info("limited: %s", limited)
        if limited:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Chill out!"
            )

    return dependency


