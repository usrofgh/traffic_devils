from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings


class BaseModel(DeclarativeBase):
    pass


engine = create_async_engine(settings.DB_DSN.get_secret_value())
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as db:
        yield db


SessionDep = Annotated[SessionLocal, Depends(get_db)]
