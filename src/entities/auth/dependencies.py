from typing import Annotated

import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError

from src.database import SessionDep
from src.entities.auth.exceptions import AuthException, AuthForbiddenException, IncorrectCredsException
from src.entities.auth.repository import SQLAuthRepository
from src.entities.auth.service import OAUTH2_SCHEME, AuthService
from src.entities.user.model import UserModel
from src.entities.user.repository import SQLUserRepository
from src.settings import settings


def get_sql_auth_service(db: SessionDep) -> AuthService:
    return AuthService(SQLAuthRepository(db))


AuthServiceObj = Annotated[AuthService, Depends(get_sql_auth_service)]


async def get_current_user(
        token: Annotated[str, Depends(OAUTH2_SCHEME)],
        db: SessionDep,
) -> UserModel:
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.JWT_ACCESS_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthException
    except InvalidTokenError:
        raise IncorrectCredsException

    db_user = await SQLUserRepository(db).find_one(id=user_id)
    if not db_user:
        raise AuthForbiddenException
    return db_user


async def get_current_manager_user(db_user: UserModel = Depends(get_current_user)) -> UserModel:
    if db_user.role.name != "manager":
        raise AuthForbiddenException
    return db_user


async def get_current_admin_user(db_user: UserModel = Depends(get_current_user)) -> UserModel:
    if db_user.role.name != "admin":
        raise AuthForbiddenException
    return db_user


async def get_current_admin_or_manager(db_user: UserModel = Depends(get_current_user)) -> UserModel:
    if db_user.role.name not in ["admin", "manager"]:
        raise AuthForbiddenException
    return db_user
