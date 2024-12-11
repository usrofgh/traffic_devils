import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from src.entities.user.exceptions import (
    PasswordMismatchException,
    PasswordNotProperException,
    UsernameSpecialSymbolsException,
)


class UserReadSchema(BaseModel):
    id: int
    username: str
    role_id: int
    registered_at: datetime


class UserFilterSchema(BaseModel):
    username: str | None = None
    role_id: int | None = None
    registered_at: datetime | None = None


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=4, max_length=50)
    password: str = Field(min_length=8, max_length=300)
    confirm_password: str = Field(min_length=8, max_length=300)

    @staticmethod
    @field_validator("confirm_password")
    def validate_password(password: str, info: FieldValidationInfo) -> str:
        if "password" in info.data and password != info.data["password"]:
            raise PasswordMismatchException

        is_upper = False
        is_digit = False
        is_special = False
        special_characters = set("!@#$%^&*(),.?\":{}|<>")

        for ch in password:
            if ch == ch.isupper():
                is_upper = True
            if ch.isdigit():
                is_digit = True
            if ch in special_characters:
                is_special = True

        if all([is_upper, is_digit, is_special]):
            return password
        else:
            raise PasswordNotProperException

    @staticmethod
    @field_validator("username")
    def validate_username(username: str) -> str:
        if not re.match("^[a-zA-Z0-9_]+$", username):
            raise UsernameSpecialSymbolsException
        return username


class UserCreateDBSchema(BaseModel):
    username: str
    password: str
    role_id: int


class UserLoginSchema(BaseModel):
    username: str
    password: str
