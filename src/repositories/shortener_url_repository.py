from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from logger import log
from models.short_urls import ShortURL
from schemas.exceptions import InternalDatabaseException
from schemas.pydantic_schemas import CreateShortURL


class ShortenerURLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_record_by_slug(self, slug: str) -> ShortURL | None:
        stmt = select(ShortURL).where(ShortURL.slug==slug)
        record = await self.session.scalar(stmt)
        return record

    async def get_record_by_full_url(self, full_url: str) -> ShortURL | None:
        stmt = select(ShortURL).where(ShortURL.full_url==full_url)
        record = await self.session.scalar(stmt)
        return record

    async def create_record(self, short_url: CreateShortURL) -> ShortURL | None:
        try:
            dict_record = short_url.model_dump()
            stmt = insert(ShortURL).values(**dict_record).returning(ShortURL)

            result = await self.session.scalar(stmt)
        except IntegrityError as e:
            log.error("Failed to save record in database: %s", e)
            await self.session.rollback()
            raise InternalDatabaseException from e
        await self.session.commit()
        return result





