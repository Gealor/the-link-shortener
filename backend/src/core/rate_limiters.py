import random
from time import time
from typing import Protocol

from redis.asyncio import Redis

from core.config import settings


class RateLimiterProtocol(Protocol):
    async def is_limited(
        self,
        ip_address: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int = settings.rate_limiter.window_size,
    ) -> bool:
        ...

class RateLimiterSlidingWindowLog:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def is_limited(
        self,
        ip_address: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int = settings.rate_limiter.window_size,
    ) -> bool:
        key = f"{settings.rate_limiter.topic_name}:{endpoint}:{ip_address}"

        now = time()*1000
        window_start = now - window_seconds * 1000

        current_request = f"{now}-{random.randint(0, 100_000)}"

        async with self._redis.pipeline(transaction=True) as pipe:
            # удаляем записи старше окна, начиная с начала времен (0) до начала текущего окна (now - window_seconds)
            await pipe.zremrangebyscore(key, 0, window_start)
            # получаем количество оставшихся элементов
            await pipe.zcard(key)
            # добавляем текущий запрос
            await pipe.zadd(key, {current_request: now})
            # ставим время жизни ключа, чтобы по прошествии time ключ удалялся
            await pipe.expire(key, time=settings.rate_limiter.ttl_seconds)
            results = await pipe.execute()

        _, current_count, _, _ = results
        return current_count >= max_requests


# Плюсы: высокая производительность и экономия памяти
# Минусы: не совсем точно (погрешность ~1%)
class RateLimiterSlidingWindowCounter:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def is_limited(
        self,
        ip_address: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int = settings.rate_limiter.window_size,
    ) -> bool:
        key_prefix = f"{settings.rate_limiter.topic_name}:{endpoint}:{ip_address}"

        now = int(time()*1000)
        window_size_ms = window_seconds * 1000

        curr_window_start = (now // window_size_ms) * window_size_ms
        prev_window_start = curr_window_start - window_size_ms

        curr_key = f"{key_prefix}:{curr_window_start}"
        prev_key = f"{key_prefix}:{prev_window_start}"

        async with self._redis.pipeline(transaction=True) as pipe:
            await pipe.get(prev_key)
            await pipe.incr(curr_key)
            await pipe.expire(curr_key, window_seconds * 2)

            # Выполняем разом
            result = await pipe.execute()

        prev_count = int(result[0] or 0)
        curr_count = int(result[1])

        elapsed = now - curr_window_start
        weight = (window_size_ms - elapsed) / window_size_ms
        estimated_count = (prev_count * weight) + curr_count

        return estimated_count > max_requests



