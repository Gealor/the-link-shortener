from unittest.mock import AsyncMock, MagicMock

import pytest

from models.short_urls import ShortURL
from schemas.exceptions import OutOfAttemptsForRepeatException, SlugAlreadyExistsException, URLBySlugDontExistException
from services.shortener_service import ShortenerService

TEST_SLUG = "aaa"
TEST_URL = "https://test@example.ru/"


@pytest.fixture()
def service_with_mock_db(shortener_service: ShortenerService):
    shortener_service.repo = AsyncMock()
    return shortener_service

@pytest.mark.parametrize(
    "len_code",
    [0, 1, 2, 6,]
)
def test_generate_random_code(service_with_mock_db: ShortenerService, len_code: int):
    result = service_with_mock_db._generate_random_code(length=len_code)
    assert len(result) == len_code


async def test_generate_code_without_repeating_success(service_with_mock_db: ShortenerService, mocker):
    service_with_mock_db.repo.get_record_by_slug.return_value = None

    result = await service_with_mock_db._generate_code_without_repeating()
    assert isinstance(result, str)
    assert len(result)==6


async def test_generate_code_without_repeating_failed(service_with_mock_db: ShortenerService):
    service_with_mock_db._generate_random_code = MagicMock(return_value=TEST_SLUG)
    service_with_mock_db.repo.get_record_by_slug.return_value = ShortURL(
        slug=TEST_SLUG,
        full_url=TEST_URL
    )

    with pytest.raises(OutOfAttemptsForRepeatException):
        result = await service_with_mock_db._generate_code_without_repeating()


async def test_get_full_url_by_slug_success(service_with_mock_db: ShortenerService):
    service_with_mock_db.repo.get_record_by_slug.return_value = ShortURL(
        slug=TEST_SLUG,
        full_url=TEST_URL
    )

    result = await service_with_mock_db.get_full_url_by_slug(code = TEST_SLUG)
    assert result is not None
    assert result.slug == TEST_SLUG
    assert str(result.full_url) == TEST_URL
    assert isinstance(result.full_slug, str)


async def test_get_full_url_by_slug_failed(service_with_mock_db):
    service_with_mock_db.repo.get_record_by_slug.return_value = None

    with pytest.raises(URLBySlugDontExistException):
        await service_with_mock_db.get_full_url_by_slug(code = TEST_SLUG)
