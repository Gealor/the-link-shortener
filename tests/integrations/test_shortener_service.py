from unittest.mock import AsyncMock, MagicMock
import pytest
from pydantic import HttpUrl

from models.short_urls import ShortURL
from schemas.exceptions import OutOfAttemptsForRepeatException, URLBySlugDontExistException
from schemas.pydantic_schemas import URLShort
from services.shortener_service import ShortenerService


@pytest.fixture()
def http_urls():
    records = [
        HttpUrl("https://example.com"),
        HttpUrl("http://example.com/path/to/resource"),
        HttpUrl("https://www.google.com/search?q=pytest"),
        HttpUrl("https://sub.domain.example.org/api/v1/resource?id=123"),
        HttpUrl("https://example.com/path?param1=value1&param2=value2"),
    ]
    return records


async def test_generate_and_safe_shortcut_url_success(shortener_service: ShortenerService, http_urls: list[HttpUrl]):
    index = 0

    created_result = await shortener_service.generate_and_safe_shortcut_url(url = http_urls[index])
    assert created_result is not None
    assert isinstance(created_result, URLShort)
    assert created_result.full_url == http_urls[0]

    result = await shortener_service.repo.get_record_by_slug(slug = created_result.slug)
    assert result is not None
    assert result.slug == created_result.slug
    assert result.full_url == str(created_result.full_url)


@pytest.mark.parametrize(
    "index",
    [0, 1, 2, 3, 4]
)
async def test_generate_and_safe_shortcut_url_success_without_creating(
    shortener_service: ShortenerService,
    shortener_records: list[ShortURL],
    index: int,
):
    result = await shortener_service.get_full_url_by_slug(code = shortener_records[index].slug)
    assert result is not None
    assert result.slug == shortener_records[index].slug
    assert result.full_url == HttpUrl(shortener_records[index].full_url)

    shortener_service.repo.create_record = AsyncMock()
    result = await shortener_service.generate_and_safe_shortcut_url(url = HttpUrl(shortener_records[index].full_url))

    shortener_service.repo.create_record.assert_not_called()
    assert result is not None
    assert result.full_url == HttpUrl(shortener_records[index].full_url)
    assert result.slug == shortener_records[index].slug

async def test_generate_and_safe_shortcut_url_failed(
    shortener_service: ShortenerService,
    shortener_records: list[ShortURL],
):
    index = 0
    shortener_service._generate_random_code = MagicMock(return_value = shortener_records[0].slug)

    with pytest.raises(OutOfAttemptsForRepeatException):
        await shortener_service.generate_and_safe_shortcut_url(url = HttpUrl("https://yandex.ru"))


async def test_get_full_url_by_slug_success(shortener_service: ShortenerService, shortener_records: list[ShortURL]):
    index = 0
    result = await shortener_service.get_full_url_by_slug(code = shortener_records[0].slug)

    assert result is not None
    assert result.slug == shortener_records[index].slug
    assert result.full_url == HttpUrl(shortener_records[index].full_url)


async def test_get_full_url_by_slug_failed(shortener_service: ShortenerService):
    with pytest.raises(URLBySlugDontExistException):
        await shortener_service.get_full_url_by_slug(code = "123456")


