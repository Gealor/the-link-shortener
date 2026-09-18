from datetime import UTC
from datetime import datetime
from datetime import timedelta

from src.core.auth.creation_tokens import create_token
from src.core.auth.passwords import compare_hashed_passwords
from src.core.auth.passwords import hash_password
from src.core.config import settings
from src.core.logger import log
from src.models.users import User
from src.repositories.session_repository import SessionTokenRepository
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schemas import ResponseSchema
from src.schemas.auth_schemas import UserRegister
from src.schemas.auth_schemas import UserRegisterWithRepeatPassword
from src.schemas.exceptions import PasswordsNotMatchException
from src.schemas.exceptions import UserNotActiveException
from src.schemas.exceptions import UserNotFoundException


class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: SessionTokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def _save_session_token(self, user_id: int, token_hash: str) -> None:
        existing_token = await self.token_repo.get_token_by_user_id(user_id)
        expired_at = datetime.now(UTC) + timedelta(
            minutes=settings.auth.session_id_expire_minutes
        )
        if existing_token:
            await self.token_repo.update_record(user_id, token_hash, expired_at)
        else:
            await self.token_repo.create_record(user_id, token_hash, expired_at)

    async def register_user(
        self, user_data: UserRegisterWithRepeatPassword
    ) -> ResponseSchema:
        if user_data.password != user_data.repeat_password:
            log.error("Password and repeat password do not match")
            raise PasswordsNotMatchException

        register_data = UserRegister(**user_data.model_dump(exclude={"repeat_password"}))
        register_data.password = (await hash_password(user_data.password)).decode("utf-8")
        # NicknameAlreadyExistsException пробросит репозиторий на unique-violation
        await self.user_repo.create_user(register_data)

        return ResponseSchema(msg="Succesful registration. Now you can log in.")

    async def login_user(self, nickname: str, password: str) -> tuple[str, User]:
        user = await self.user_repo.get_user_by_nickname(nickname=nickname)
        if not user:
            log.error("User by nickname %s not found", nickname)
            raise UserNotFoundException

        is_valid = await compare_hashed_passwords(
            entered_password=password.encode("utf-8"),
            hashed_password=user.password.encode("utf-8"),
        )
        if not is_valid:
            log.error("Passwords do not match")
            raise PasswordsNotMatchException

        if not user.is_active:
            log.error("User with nickname %s is not active", nickname)
            raise UserNotActiveException

        token, token_hash = create_token()
        await self._save_session_token(user_id=user.id, token_hash=token_hash)
        log.info("Succesful log in in account: %s", nickname)
        return token, user

    async def logout_user(self, user_id: int) -> None:
        await self.token_repo.delete_token(user_id)
        log.info("User id=%d logged out, session token deleted", user_id)
