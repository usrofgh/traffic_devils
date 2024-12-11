from src.entities.auth.exceptions import AuthForbiddenException, IncorrectCredsException
from src.entities.auth.schemas import JWTLoginResponseSchema
from src.entities.auth.service import AuthService
from src.entities.role.exceptions import (
    AdminAssigmentException,
    AlreadyHaveManagerException,
    AlreadyManagerException,
    RoleNotFoundException,
    UnassignAnotherManagerException,
    YourselfAssigmentException,
)
from src.entities.role.repository import RoleRepository
from src.entities.user.exceptions import UserExistsException, UserNotFoundException
from src.entities.user.model import UserModel
from src.entities.user.repository import UserRepository
from src.entities.user.schemas import UserCreateDBSchema, UserCreateSchema, UserFilterSchema, UserLoginSchema


class UserService:
    def __init__(self, repository: UserRepository, role_repository: RoleRepository, auth_service: AuthService):
        self._repository = repository
        self._auth_service = auth_service
        self._role_repository = role_repository

    async def authenticate_user(self, login_schema: UserLoginSchema) -> UserModel:
        db_user = await self._repository.find_one(username=login_schema.username)
        if db_user:
            is_same_password = self._auth_service.verify_password(login_schema.password, db_user.password)
            if is_same_password:
                return db_user

    async def login(self, login_schema: UserLoginSchema) -> JWTLoginResponseSchema:
        db_user = await self.authenticate_user(login_schema)
        if not db_user:
            raise IncorrectCredsException

        token_data = self._auth_service.generate_tokens(db_user.id)
        await self._auth_service.save_token(user_id=db_user.id, refresh_token=token_data.refresh_token)

        return token_data

    async def create_user(self, create_schema: UserCreateSchema) -> UserModel:
        db_user = await self._repository.find_one(username=create_schema.username)
        if db_user:
            raise UserExistsException

        db_role = await self._role_repository.find_one(name="user")
        db_schema = UserCreateDBSchema(**create_schema.model_dump(), role_id=db_role.id)
        db_schema.password = self._auth_service.get_password_hash(db_schema.password)
        return await self._repository.add_one(db_schema)

    async def get_user_by_id(self, user_id: int) -> UserModel:
        db_user = await self._repository.find_one(id=user_id)
        if not db_user:
            raise UserNotFoundException
        return db_user

    async def get_users(self, filter_schema: UserFilterSchema) -> list[UserModel]:
        return await self._repository.find_all(**filter_schema.model_dump(exclude_none=True))

    async def delete_user(self, curr_user: UserModel, user_id: int) -> None:
        if user_id != curr_user.id and curr_user.role.name != "admin":
            raise AuthForbiddenException

        db_user = await self._repository.find_one(id=user_id)
        if not db_user:
            raise UserNotFoundException

        await self._repository.delete(db_user)

    async def assign_manager(self, curr_user: UserModel, user_id: int):
        if curr_user.role.name not in ["admin", "manager"]:
            raise AuthForbiddenException

        if curr_user.id == user_id:
            raise YourselfAssigmentException

        db_client = await self.get_user_by_id(user_id)
        if not db_client:
            raise UserNotFoundException
        elif db_client.role.name in ["admin", "manager"]:
            raise AdminAssigmentException
        elif db_client.manager_id == curr_user.id:
            raise AlreadyManagerException
        elif db_client.manager_id:
            raise AlreadyHaveManagerException

        db_client.manager_id = curr_user.id
        await self._repository.db.commit()

    async def unassign_manager(self, curr_user: UserModel, user_id: int):
        db_client = await self.get_user_by_id(user_id)
        if db_client.manager_id != curr_user.id:
            raise UnassignAnotherManagerException

        db_client.manager_id = None
        await self._repository.db.commit()

    async def change_role(self, user_id: int, role: str):
        db_role = await self._role_repository.find_one(name=role)
        if not db_role:
            raise RoleNotFoundException

        db_client = await self.get_user_by_id(user_id)
        if not db_client:
            raise UserNotFoundException

        db_client.role_id = db_role.id
        await self._repository.db.commit()
