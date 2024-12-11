from abc import ABC, abstractmethod

from sqlalchemy import or_, select

from src.entities.base_repository import BaseRepository, SQLRepository
from src.entities.message.model import MessageModel


class MessageRepository(BaseRepository, ABC):
    MODEL = MessageModel

    @abstractmethod
    async def get_messages(
            self,
            author_ids: list,
            offset: int = None,
            limit: int = None,
            **filters
    ) -> list[MessageModel]:
        ...


class SQLMessageRepository(MessageRepository, SQLRepository):
    MODEL = MessageModel

    async def get_messages(
            self,
            author_ids: list = None,
            offset: int = None,
            limit: int = None,
            **filters
    ) -> list[MessageModel]:
        stmt = select(self.MODEL).filter_by(**filters)

        if author_ids:
            stmt = stmt.where(or_(*[self.MODEL.author_id == author_id for author_id in author_ids]))

        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        results = await self.db.execute(stmt)
        return results.scalars().all()
