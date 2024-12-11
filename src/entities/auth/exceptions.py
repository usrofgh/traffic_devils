from fastapi import status

from src.entities.base_exception import BException


class AuthException(BException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Could not validate credentials"


class IncorrectCredsException(BException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Incorrect credentials"


class JWTIncorrectFormatException(BException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Incorrect JWT token format"


class JWTokenExpiredException(BException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "JWT token expired"

class AuthForbiddenException(BException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Not enough rules"
