from fastapi import status

from src.entities.base_exception import BException


class UserNotFoundException(BException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "User not found"


class UserExistsException(BException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "User already exists"


class PasswordMismatchException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Passwords do not match"


class PasswordNotProperException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Password must contain at least: one uppercase letter, one special character, one digit"


class UsernameSpecialSymbolsException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Username can only contain alphanumeric characters and underscores"
