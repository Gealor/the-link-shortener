from core.database import async_session_maker


async def db_session_getter():
    async with async_session_maker() as session:
        yield session
