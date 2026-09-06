import asyncio
import random
from functools import wraps
from typing import Awaitable
from typing import Callable
from typing import ParamSpec
from typing import TypeVar

from src.core.config import settings
from src.core.logger import log
from src.schemas.exceptions import OutOfAttemptsForRepeatException

P = ParamSpec("P")
R = TypeVar("R")

def repeat_decorator(count: int = settings.count_repeating):
    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: Exception | None = None
            for attempt in range(1, count + 1):
                try:
                    result = await func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    log.warning("Failed to execute function (attempt %d/%d): %s", attempt, count, e)
                    if attempt < count:
                        sleep_time = settings.backoff_factor ** attempt + random.uniform(0, 1)
                        await asyncio.sleep(sleep_time)
                else:
                    return result
            raise OutOfAttemptsForRepeatException from last_exc
        return wrapper
    return decorator
