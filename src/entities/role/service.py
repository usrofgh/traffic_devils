from src.entities.role.exceptions import RoleExistsException, RoleNotFoundException
from src.entities.role.model import RoleModel
from src.entities.role.repository import RoleRepository
from src.entities.role.schemas import RoleCreateSchema, RoleFilterSchema


class RoleService:
    def __init__(self, repository: RoleRepository):
        self._repository = repository

    async def create_role(self, create_schema: RoleCreateSchema) -> RoleModel:
        db_role = await self._repository.find_one(name=create_schema.name)
        if db_role:
            raise RoleExistsException

        return await self._repository.add_one(create_schema)

    async def delete_role(self, role_id: int) -> None:
        db_role = await self._repository.find_one(id=role_id)
        if not db_role:
            raise RoleNotFoundException

        await self._repository.delete(db_role)

    async def get_roles(self, filter_schema: RoleFilterSchema) -> list[RoleModel]:
        return await self._repository.find_all(**filter_schema.model_dump(exclude_none=True))

    async def get_role_by_id(self, role_id: int) -> RoleModel:
        db_role = await self._repository.find_one(id=role_id)
        if not db_role:
            raise RoleNotFoundException
        return db_role
