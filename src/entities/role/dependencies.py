from typing import Annotated

from fastapi import Depends

from src.database import SessionDep
from src.entities.role.repository import SQLRoleRepository
from src.entities.role.service import RoleService


async def get_sql_role_service(db: SessionDep) -> RoleService:
    return RoleService(SQLRoleRepository(db))


RoleServiceObj = Annotated[RoleService, Depends(get_sql_role_service)]


