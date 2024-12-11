from abc import ABC

from src.entities.base_repository import BaseRepository, SQLRepository
from src.entities.user.model import UserModel


class UserRepository(BaseRepository, ABC):
    pass


class SQLUserRepository(UserRepository, SQLRepository):
    MODEL = UserModel
