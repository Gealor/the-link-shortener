import string
from random import choice

from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from logger import log
from repositories.shortener_url_repository import ShortenerURLRepository
from schemas.exceptions import SlugAlreadyExistsException
from schemas.pydantic_schemas import CreateShortURL
from schemas.pydantic_schemas import URLShort
from utils.decorators import repeat_decorator

ALPHABET: str = string.ascii_letters + string.digits

class ShortenerService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ShortenerURLRepository(session=self.session)

    def _generate_random_code(self) -> str:
        return "".join([choice(ALPHABET) for _ in range(6)])

    @repeat_decorator()
    async def _generate_code_without_repeating(self) -> str:
        code = self._generate_random_code()
        found_record = await self.repo.get_record_by_slug(code)
        if found_record and found_record.slug == code:
            raise SlugAlreadyExistsException("This slug already exist.")
        return code

    async def generate_and_safe_shortcut_url(self, url: HttpUrl) -> URLShort:
        str_url = str(url)
        if record := await self.repo.get_record_by_full_url(full_url=str_url):
            log.info("Slug with these url already exist. Return existed record")
            return URLShort(
                full_url=url, 
                slug=record.slug,
            )

        code = await self._generate_code_without_repeating()

        created_record = CreateShortURL(
            full_url=str_url,
            slug=code
        )
        record = await self.repo.create_record(short_url=created_record)
        log.info("Generated slug %s for url: %s", code, url)

        return URLShort.model_validate(record)




