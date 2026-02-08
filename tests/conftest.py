from typing import AsyncGenerator
from typing import Generator

import pytest
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from testcontainers.postgres import PostgresContainer

from models.base import Base
from models.short_urls import ShortURL
from repositories.shortener_url_repository import ShortenerURLRepository
from services.shortener_service import ShortenerService


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer(
        "postgres:15"
        # "postgis/postgis:15-3.3"
    ) as postgres:
        yield postgres

def create_db_url(postgres_container) -> str:
    raw_url: str = postgres_container.get_connection_url()
    asyncpg_url = raw_url.replace("postgresql+psycopg2", "postgresql+asyncpg", 1)
    print(asyncpg_url)
    return asyncpg_url

@pytest.fixture(scope="session")
async def engine(postgres_container) -> AsyncGenerator[AsyncEngine, None]:
    """Create the database engine and tables once for the entire test session."""
    db_url = create_db_url(postgres_container)
    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()

@pytest.fixture(scope="function")
async def async_session(engine) -> AsyncGenerator[AsyncSession, None]:
    """Creates a new session and rolls back all changes for full test isolation."""
    async_session_factory = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    connection = await engine.connect()  # Get a new DB connection
    transaction = await connection.begin()  # Start an outer transaction

    session = async_session_factory(bind=connection)  # Bind session to this connection
    await session.begin_nested()  # Begin a SAVEPOINT for test isolation

    try:
        yield session  # Test runs inside this session
    finally:
        await session.rollback()  # Rollback all changes made by the test
        await transaction.rollback()  # Ensure the outer transaction is also rolled back
        await connection.close()  # Close connection after test completion
        await session.close()  # Explicitly close the session

@pytest.fixture()
def shortener_repository(async_session):
    return ShortenerURLRepository(session=async_session)

@pytest.fixture()
def shortener_service(shortener_repository):
    return ShortenerService(repo=shortener_repository)


@pytest.fixture()
async def shortener_records(async_session: AsyncSession):
    records = [
        ShortURL(
            slug="aZ3kP9",
            full_url = str(HttpUrl("https://example.com"))
        ),
        ShortURL(
            slug = "Q7m2Xe",
            full_url = str(HttpUrl("http://example.com/path/to/resource")),
        ),
        ShortURL(
            slug = "9fKpL2",
            full_url = str(HttpUrl("https://www.google.com/search?q=pytest")),
        ),
        ShortURL(
            slug = "M4xAq8",
            full_url = str(HttpUrl("https://sub.domain.example.org/api/v1/resource?id=123")),
        ),
        ShortURL(
            slug = "c7RZ1B",
            full_url = str(HttpUrl("https://example.com/path?param1=value1&param2=value2")),
        ),
    ]
    async_session.add_all(records)
    await async_session.commit()
    return records
