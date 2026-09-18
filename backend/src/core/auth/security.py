from datetime import UTC
from datetime import datetime

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status

from src.core.auth.creation_tokens import hash_token
from src.core.config import settings
from src.core.cookies import get_value_from_cookie
from src.core.logger import log
from src.repositories import get_session_token_repository
from src.repositories.session_repository import SessionTokenRepository
from src.schemas.auth_schemas import UserRead

_UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
)


def _get_session_from_cookie(request: Request) -> str | None:
    return get_value_from_cookie(settings.auth.session_id_cookie_name, request)


async def get_current_user(
    token: str | None = Depends(_get_session_from_cookie),
    token_repo: SessionTokenRepository = Depends(get_session_token_repository),
) -> UserRead:
    if not token:
        log.info("Session cookie is not set")
        raise _UNAUTHORIZED

    token_hash = hash_token(token)
    token_record = await token_repo.get_token_by_hash(token_hash, load_user=True)
    if token_record is None:
        log.info("Session token not found")
        raise _UNAUTHORIZED

    if datetime.now(UTC) >= token_record.expired_at:
        log.info("Session token expired for user_id=%d", token_record.user_id)
        raise _UNAUTHORIZED

    user = UserRead.model_validate(token_record.user)
    if not user.is_active:
        log.info("User with id=%d is not active", user.id)
        raise _UNAUTHORIZED

    return user
