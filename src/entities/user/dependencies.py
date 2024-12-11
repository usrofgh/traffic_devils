from typing import Annotated

from fastapi import Depends

from src.database import SessionDep
from src.entities.auth.dependencies import AuthServiceObj
from src.entities.role.repository import SQLRoleRepository
from src.entities.user.repository import SQLUserRepository
from src.entities.user.service import UserService


def get_sql_user_service(
        db: SessionDep,
        auth_service: AuthServiceObj
) -> UserService:
    return UserService(SQLUserRepository(db), SQLRoleRepository(db), auth_service)


UserServiceObj = Annotated[UserService, Depends(get_sql_user_service)]
