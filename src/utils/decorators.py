from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

from schemas.exceptions import BaseShortnererUrlException
from core.config import settings
from logger import log

P = ParamSpec("P")
R = TypeVar("R")

def repeat_decorator(count: int = settings.count_repeating):
    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            remaining_attempts = count
            while remaining_attempts:
                try:
                    result = await func(*args, **kwargs)
                except Exception as e:
                    log.warning("Failed to execute function: %s", e)
                    remaining_attempts-=1
                else:
                    return result
            raise BaseShortnererUrlException
        return wrapper
    return decorator
                