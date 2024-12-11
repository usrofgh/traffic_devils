from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.database import BaseModel
from src.entities.role.model import RoleModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    registered_at: Mapped[datetime] = mapped_column(server_default=func.now())
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    clients: Mapped[list["UserModel"]] = relationship(lazy="selectin", join_depth=1)

    messages: Mapped[list["MessageModel"]] = relationship(back_populates="author", cascade="all, delete")
    refresh_token: Mapped["AuthTokenModel"] = relationship(back_populates="user", cascade="all, delete")
    role: Mapped["RoleModel"] = relationship(back_populates="users", lazy="selectin")
