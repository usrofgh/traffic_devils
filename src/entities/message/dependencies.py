from typing import Annotated

from fastapi import Depends

from src.database import SessionDep
from src.entities.message.repository import SQLMessageRepository
from src.entities.message.service import MessageService


async def get_sql_message_service(db: SessionDep) -> MessageService:
    return MessageService(SQLMessageRepository(db))

MessageServiceObj = Annotated[MessageService, Depends(get_sql_message_service)]
