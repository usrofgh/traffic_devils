from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import select

SchemaType = TypeVar("SchemaType", bound=BaseModel)
DBSession = TypeVar("DBSession")


class BaseRepository(ABC):
    MODEL = None

    def __init__(self, db: DBSession):
        self.db = db

    @abstractmethod
    async def add_one(self, schema: SchemaType) -> MODEL:
        ...

    @abstractmethod
    async def find_one(self, **filters) -> MODEL:
        ...

    @abstractmethod
    async def find_all(self, **filters) -> list[MODEL]:
        ...

    @abstractmethod
    async def update(self, db_obj: MODEL, schema: SchemaType) -> MODEL:
        ...

    @abstractmethod
    async def delete(self, db_obj: MODEL) -> None:
        ...


class SQLRepository(BaseRepository, ABC):
    MODEL = None

    async def add_one(self, schema: SchemaType) -> MODEL:
        db_obj = self.MODEL(**schema.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def find_one(self, **filters) -> MODEL:
        stmt = select(self.MODEL).filter_by(**filters)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def find_all(self, offset: int = None, limit: int = None, **filters) -> list[MODEL]:
        stmt = select(self.MODEL).filter_by(**filters)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, db_obj: MODEL, schema: SchemaType) -> MODEL:
        obj_data = schema.model_dump(exclude_unset=True)  # Only update provided fields
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: MODEL) -> None:
        await self.db.delete(db_obj)
        await self.db.commit()
