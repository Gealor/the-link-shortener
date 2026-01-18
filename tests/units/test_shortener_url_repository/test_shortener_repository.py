import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.short_urls import ShortURL
from repositories.shortener_url_repository import ShortenerURLRepository
from schemas.pydantic_schemas import CreateShortURL


@pytest.fixture()
def created_record():
    return CreateShortURL(
        slug = "T2eWn9",
        full_url = "http://localhost:8080/test",
    )


async def test_create_record(shortener_repository: ShortenerURLRepository, created_record: CreateShortURL):
    result = await shortener_repository.create_record(short_url=created_record)

    assert result is not None
    assert isinstance(result, ShortURL)

    get_record = await shortener_repository.get_record_by_slug(slug = created_record.slug)
    assert get_record is not None
    assert isinstance(get_record, ShortURL)
    assert get_record.slug == result.slug
    assert get_record.full_url == result.full_url


async def test_get_record_by_slug_success(shortener_repository: ShortenerURLRepository, shortener_records: list[ShortURL]):
    index = 0
    result = await shortener_repository.get_record_by_slug(slug = shortener_records[index].slug)

    assert result is not None
    assert result.slug == shortener_records[index].slug
    assert result.full_url == shortener_records[index].full_url


async def test_get_record_by_slug_none(shortener_repository: ShortenerURLRepository):
    result = await shortener_repository.get_record_by_slug(slug = "1234")

    assert result is None


async def test_get_record_by_full_url(shortener_repository: ShortenerURLRepository, shortener_records: list[ShortURL]):
    index = 0
    result = await shortener_repository.get_record_by_full_url(full_url= shortener_records[index].full_url)

    assert result is not None
    assert result.slug == shortener_records[index].slug
    assert result.full_url == shortener_records[index].full_url


async def test_get_record_by_full_url_none(shortener_repository: ShortenerURLRepository):
    result = await shortener_repository.get_record_by_full_url(full_url = "https://yandex.ru")

    assert result is None
