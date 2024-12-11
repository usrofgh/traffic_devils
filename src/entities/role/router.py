from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from pydantic import conint
from src.entities.auth.dependencies import get_current_admin_or_manager, get_current_admin_user
from src.entities.role.dependencies import RoleServiceObj
from src.entities.role.schemas import RoleCreateSchema, RoleFilterSchema, RoleReadSchema, RoleReadByIdSchema

role_router = APIRouter(
    prefix="/roles",
    tags=["Role"]
)


@role_router.post(
    path="",
    response_model=RoleReadSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)]
)
async def create_role(role_service: RoleServiceObj, create_schema: RoleCreateSchema):
    return await role_service.create_role(create_schema)


@role_router.get(
    path="",
    response_model=list[RoleReadSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_admin_or_manager)]
)
async def get_roles(role_service: RoleServiceObj, filter_schema: Annotated[RoleFilterSchema, Query()]):
    return await role_service.get_roles(filter_schema)


@role_router.get(
    path="/{role_id}",
    response_model=RoleReadSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_admin_or_manager)]
)
async def get_role(role_service: RoleServiceObj, role_id: int):
    return await role_service.get_role_by_id(role_id)


@role_router.delete(
    path="/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)]
)
async def delete_role(role_service: RoleServiceObj, role_id: int):
    await role_service.delete_role(role_id)
