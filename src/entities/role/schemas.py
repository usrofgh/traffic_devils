from pydantic import BaseModel, Field


class RoleReadSchema(BaseModel):
    id: int
    name: str


class RoleCreateSchema(BaseModel):
    name: str


class RoleFilterSchema(BaseModel):
    name: str | None = None
    offset: int | None  = Field(ge=0, default=None)
    limit: int | None  = Field(ge=0, default=None)

class RoleReadByIdSchema(BaseModel):
    id: int = Field(ge=0)
