from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import create_engine, Engine

from .config import settings


engine = create_engine(
    url=settings.database.db_url,
    echo=settings.database.db_echo,
)

async_session_maker = async_sessionmaker(bind=engine)

async def db_session_getter():
    async with async_session_maker() as session:
        yield session