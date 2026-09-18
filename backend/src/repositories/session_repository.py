from datetime import datetime

from sqlalchemy import Select
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.logger import log
from src.models.sessions import SessionToken
from src.schemas.exceptions import AuthDatabaseException
from src.schemas.exceptions import SessionTokenNotFoundException


class SessionTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _load_user(self, stmt: Select) -> Select:
        # joinedload подгружает связь через join (одним запросом вместе с токеном)
        return stmt.options(joinedload(SessionToken.user))

    async def get_token_by_user_id(self, user_id: int) -> str | None:
        stmt = select(SessionToken.session_token).where(SessionToken.user_id == user_id)
        return await self.session.scalar(stmt)

    async def get_token_by_hash(
        self, token_hash: str, load_user: bool = False
    ) -> SessionToken | None:
        stmt = select(SessionToken).where(SessionToken.session_token == token_hash)
        if load_user:
            stmt = self._load_user(stmt)
        return await self.session.scalar(stmt)

    async def create_record(
        self, user_id: int, token_hash: str, expired_at: datetime
    ) -> None:
        record = SessionToken(
            user_id=user_id,
            session_token=token_hash,
            expired_at=expired_at,
        )
        self.session.add(record)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            log.error("Failed to add session_token: %s", e)
            raise AuthDatabaseException from e

        await self.session.refresh(record)
        log.info("Add session token for user with id=%s", record.user_id)

    async def update_record(
        self, user_id: int, token_hash: str, expired_at: datetime
    ) -> str:
        stmt = (
            update(SessionToken)
            .values(session_token=token_hash, expired_at=expired_at)
            .where(SessionToken.user_id == user_id)
            .returning(SessionToken)
        )
        record = await self.session.scalar(stmt)
        if record is None:
            raise SessionTokenNotFoundException

        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            log.error("Failed to update session_token: %s", e)
            raise AuthDatabaseException from e

        await self.session.refresh(record)
        log.info("Update session token for user_id=%d", record.user_id)
        return record.session_token

    async def delete_token(self, user_id: int) -> None:
        stmt = delete(SessionToken).where(SessionToken.user_id == user_id)
        await self.session.execute(stmt)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            log.error("Failed to delete session token: %s", e)
            raise AuthDatabaseException from e

        log.info("Deleted session token with user_id=%d", user_id)
