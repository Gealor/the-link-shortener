from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status

from src.core.auth.csrf import CSRF_Secure
from src.core.auth.csrf import issue_csrf_token
from src.core.auth.csrf import set_csrf_cache_headers
from src.core.auth.csrf import verify_csrf
from src.core.auth.security import get_current_user
from src.core.config import settings
from src.core.cookies import clear_session_cookie
from src.core.cookies import set_session_cookie
from src.core.logger import log
from src.schemas.auth_schemas import CsrfTokenResponse
from src.schemas.auth_schemas import LoginCredentials
from src.schemas.auth_schemas import ResponseSchema
from src.schemas.auth_schemas import SessionResponse
from src.schemas.auth_schemas import UserRead
from src.schemas.auth_schemas import UserRegisterWithRepeatPassword
from src.schemas.exceptions import NicknameAlreadyExistsException
from src.schemas.exceptions import PasswordsNotMatchException
from src.schemas.exceptions import UserNotActiveException
from src.schemas.exceptions import UserNotFoundException
from src.services import get_auth_service
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me")
async def me(
    current_user: Annotated[UserRead, Depends(get_current_user)],
) -> UserRead:
    """Вернуть текущего пользователя по куке сессии (или 401)."""
    return current_user


@router.get("/csrf", dependencies=[Depends(get_current_user)])
async def get_csrf_token(
    response: Response,
    csrf_protect: CSRF_Secure,
) -> CsrfTokenResponse:
    csrf_token = issue_csrf_token(csrf_protect, response)
    # set_csrf_cache_headers(response)
    return CsrfTokenResponse(csrf_token=csrf_token)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegisterWithRepeatPassword,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> ResponseSchema:
    try:
        return await service.register_user(user_data)
    except PasswordsNotMatchException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        ) from exc
    except NicknameAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This nickname is already taken",
        ) from exc


@router.post("/login")
async def login(
    credentials: LoginCredentials,
    response: Response,
    csrf_protect: CSRF_Secure,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> SessionResponse:
    try:
        token, user = await service.login_user(
            nickname=credentials.nickname,
            password=credentials.password,
        )
    except (UserNotFoundException, PasswordsNotMatchException) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid nickname or password",
        ) from exc
    except UserNotActiveException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is blocked",
        ) from exc

    set_session_cookie(
        key=settings.auth.session_id_cookie_name,
        value=token,
        response=response,
    )
    csrf_token = issue_csrf_token(csrf_protect, response)
    log.info("User %s logged in", credentials.nickname)
    return SessionResponse(user=UserRead.model_validate(user), csrf_token=csrf_token)


@router.post("/logout", dependencies=[Depends(verify_csrf)])
async def logout(
    response: Response,
    csrf_protect: CSRF_Secure,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> ResponseSchema:
    await service.logout_user(user_id=current_user.id)
    clear_session_cookie(
        key=settings.auth.session_id_cookie_name,
        response=response,
    )
    csrf_protect.unset_csrf_cookie(response=response)
    return ResponseSchema(msg="Successfully logged out.")
