from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import log
from src.models.users import User
from src.schemas.auth_schemas import UserRegister
from src.schemas.exceptions import AuthDatabaseException
from src.schemas.exceptions import NicknameAlreadyExistsException


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_nickname(self, nickname: str) -> User | None:
        stmt = select(User).where(User.nickname == nickname)
        return await self.session.scalar(stmt)

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return await self.session.scalar(stmt)

    async def create_user(self, user_data: UserRegister) -> User:
        user = User(
            nickname=user_data.nickname,
            password=user_data.password,
            is_active=True,
        )
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            # SQLAlchemy оборачивает ошибку драйвера, оригинал лежит в e.orig.__cause__
            orig = e.orig.__cause__
            if isinstance(orig, UniqueViolationError):
                log.error("Failed to create user, unique violation: %s", orig.constraint_name)
                raise NicknameAlreadyExistsException from e
            log.error("Failed to create user: %s", e)
            raise AuthDatabaseException from e

        await self.session.refresh(user)
        log.info("Create new user with id=%d", user.id)
        return user
