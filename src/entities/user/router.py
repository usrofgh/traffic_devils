from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.entities.auth.dependencies import get_current_admin_or_manager, get_current_admin_user, get_current_user
from src.entities.user.dependencies import UserServiceObj
from src.entities.user.schemas import UserCreateSchema, UserFilterSchema, UserReadSchema

user_router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@user_router.post(
    path="/",
    response_model=UserReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user_service: UserServiceObj,
        create_schema: UserCreateSchema
):
    return await user_service.create_user(create_schema)


@user_router.get(
    path="/",
    response_model=list[UserReadSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_admin_or_manager)],
)
async def get_users(
        user_service: UserServiceObj,
        filter_schema: Annotated[UserFilterSchema, Query()]
):
    return await user_service.get_users(filter_schema)

@user_router.get(
    path="/{user_id}",
    response_model=UserReadSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_admin_or_manager)]
)
async def get_user(
        user_service: UserServiceObj,
        user_id: int
):
    return await user_service.get_user_by_id(user_id)

@user_router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
        user_service: UserServiceObj,
        user_id: int,
        curr_user = Depends(get_current_user),
):
    await user_service.delete_user(curr_user, user_id)


@user_router.get(
    path="/{user_id}/assign-manager",
    status_code=status.HTTP_200_OK
)
async def assign_manager(
        user_service: UserServiceObj,
        user_id: int,
        curr_user = Depends(get_current_admin_or_manager)
):
    await user_service.assign_manager(curr_user, user_id)


@user_router.delete(
    path="/{user_id}/unassign-manager",
    status_code=status.HTTP_204_NO_CONTENT
)
async def unassign_manager(
        user_service: UserServiceObj,
        user_id: int,
        curr_user = Depends(get_current_user)
):
    await user_service.unassign_manager(curr_user, user_id)

@user_router.patch(
    path="/{user_id}/change-role",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)]
)
async def change_role(
        user_service: UserServiceObj,
        user_id: int,
        role: str,
):
    await user_service.change_role(user_id, role)
