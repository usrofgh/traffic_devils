from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.entities.auth.dependencies import get_current_user
from src.entities.message.dependencies import MessageServiceObj
from src.entities.message.schemas import MessageCreateSchema, MessageFilterSchema, MessageReadSchema

message_router = APIRouter(
    prefix="/messages",
    tags=["Message"]
)
@message_router.post(
    path="/",
    response_model=MessageReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_message(
        message_service: MessageServiceObj,
        create_schema: MessageCreateSchema,
        curr_user = Depends(get_current_user),
):
    return await message_service.create_message(create_schema, curr_user.id)


@message_router.get(
    path="/",
    response_model=list[MessageReadSchema],
    status_code=status.HTTP_200_OK
)
async def get_messages(
        message_service: MessageServiceObj,
        filter_schema: Annotated[MessageFilterSchema, Query()],
        curr_user = Depends(get_current_user)
):
    return await message_service.get_messages(filter_schema, curr_user)


@message_router.get(
    path="/{message_id}",
    response_model=MessageReadSchema,
    status_code=status.HTTP_200_OK
)
async def get_message(
        message_service: MessageServiceObj,
        message_id: int,
        curr_user = Depends(get_current_user)

):
    return await message_service.get_message_by_id(message_id, curr_user)


@message_router.delete(
    path="/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_message(
        message_service: MessageServiceObj,
        message_id: int,
        curr_user = Depends(get_current_user)
):
    return await message_service.delete_message(message_id, curr_user)
