import datetime
from datetime import timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jwt import DecodeError
from passlib.context import CryptContext

from src.entities.auth.exceptions import IncorrectCredsException, JWTIncorrectFormatException, JWTokenExpiredException
from src.entities.auth.model import AuthTokenModel
from src.entities.auth.repository import AuthRepository
from src.entities.auth.schemas import JWTLoginResponseSchema, RefreshTokenCreateSchema
from src.settings import settings

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")

class AuthService:
    def __init__(self, repository: AuthRepository):
        self._repository = repository

    @staticmethod
    def get_password_hash(password: str) -> str:
        return PWD_CONTEXT.hash(password)

    @staticmethod
    def verify_password(plain_password: str, password: str) -> bool:
        return PWD_CONTEXT.verify(plain_password, password)

    @staticmethod
    def _create_jwt_token(data: dict, secret_key: str, type_: str, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
        else:
            expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire, "type": type_})
        encoded_jwt = jwt.encode(to_encode, secret_key, settings.JWT_ALGORITHM)
        return encoded_jwt

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        token = self._create_jwt_token(data, settings.JWT_ACCESS_KEY.get_secret_value(), "access", expires_delta)
        return token

    def create_refresh_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        token = self._create_jwt_token(data, settings.JWT_REFRESH_KEY.get_secret_value(), "refresh",expires_delta)
        return token

    @staticmethod
    def validate_access_token(token: str) -> bool:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_ACCESS_KEY,
                settings.JWT_ALGORITHM
            )
            if payload["type"] != "access":
                raise JWTIncorrectFormatException

        except JWTError:
            raise JWTIncorrectFormatException

        exp = payload.get("exp")
        if (not exp) or (exp < datetime.datetime.now(datetime.UTC)).timestamp():
            raise JWTokenExpiredException

        return payload

    @staticmethod
    def validate_refresh_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_REFRESH_KEY.get_secret_value(),
                algorithms=[settings.JWT_ALGORITHM]
            )
            if payload["type"] != "refresh":
                raise JWTIncorrectFormatException

        except (DecodeError, JWTError):
            raise JWTIncorrectFormatException

        exp = payload.get("exp")
        if (not exp) or (exp < datetime.datetime.now(datetime.UTC).timestamp()):
            raise JWTokenExpiredException

        return payload

    async def refresh_token(self, refresh_token: str) -> JWTLoginResponseSchema:
        payload = self.validate_refresh_token(refresh_token)
        db_token = await self._repository.find_one(refresh_token=refresh_token)

        if not (payload and db_token):
            raise IncorrectCredsException

        tokens = self.generate_tokens(payload["sub"])
        await self.save_token(user_id=payload["sub"], refresh_token=tokens.refresh_token)
        return tokens

    def generate_tokens(self, user_id: int) -> JWTLoginResponseSchema:
        data = {"sub": user_id}
        access_expires_delta = timedelta(minutes=settings.JWT_ACCESS_TTL_MIN)
        access_token = self.create_access_token(data, access_expires_delta)

        refresh_expires_delta = timedelta(minutes=settings.JWT_REFRESH_TTL_MIN)
        refresh_token = self.create_refresh_token(data, refresh_expires_delta)

        token_data = JWTLoginResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
        return token_data

    async def save_token(self, user_id: int, refresh_token: str) -> AuthTokenModel:
        db_token: AuthTokenModel = await self._repository.find_one(user_id=user_id)
        if db_token:
            db_token.refresh_token = refresh_token
            await self._repository.db.commit()
            return db_token

        token_schema = RefreshTokenCreateSchema(user_id=user_id, refresh_token=refresh_token)
        token = await self._repository.add_one(schema=token_schema)
        return token
