from abc import ABC

from src.entities.auth.model import AuthTokenModel
from src.entities.base_repository import BaseRepository, SQLRepository


class AuthRepository(BaseRepository, ABC):
    pass


class SQLAuthRepository(AuthRepository, SQLRepository):
    MODEL = AuthTokenModel
