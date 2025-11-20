import asyncio
from random import choice
import string
from logger import log
from schemas.pydantic_schemas import URLShort

ALPHABET: str = string.ascii_letters + string.digits

class ShortenerService:
    def __init__(self):
        pass

    def _generate_random_code(self) -> str:
        return "".join([choice(ALPHABET) for _ in range(6)])
    
    async def generate_and_safe_shortcut_url(self, url: str) -> URLShort:
        code = self._generate_random_code()

        log.info("Generated slug %s for url: %s", code, url)

        await asyncio.sleep(1)
        log.info("Write in DB alias")
        return URLShort(
            full_url=url, 
            slug=code,
        )


