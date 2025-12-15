from functools import wraps
from typing import Awaitable
from typing import Callable
from typing import ParamSpec
from typing import TypeVar

from core.config import settings
from logger import log
from schemas.exceptions import OutOfAttemptsForRepeatException

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
            raise OutOfAttemptsForRepeatException
        return wrapper
    return decorator
