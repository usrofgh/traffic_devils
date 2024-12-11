from abc import ABC

from src.entities.base_repository import BaseRepository, SQLRepository
from src.entities.role.model import RoleModel


class RoleRepository(BaseRepository, ABC):
    pass


class SQLRoleRepository(RoleRepository, SQLRepository):
    MODEL = RoleModel
