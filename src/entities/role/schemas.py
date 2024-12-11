from pydantic import BaseModel


class RoleReadSchema(BaseModel):
    id: int
    name: str


class RoleCreateSchema(BaseModel):
    name: str


class RoleFilterSchema(BaseModel):
    name: str | None = None
    offset: int | None = None
    limit: int | None = None
