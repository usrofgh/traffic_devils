from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import BaseModel


class RoleModel(BaseModel):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[list["UserModel"]] = relationship(
        back_populates="role", cascade="all, delete"
    )
