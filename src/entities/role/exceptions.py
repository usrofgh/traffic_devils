from fastapi import status

from src.entities.base_exception import BException


class RoleExistsException(BException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "Role exists"


class RoleNotFoundException(BException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Role not found"


class AlreadyManagerException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Already a manager of this user"


class AlreadyHaveManagerException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "The user already has another manager"

class YourselfAssigmentException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Impossible assign yourself"

class AdminAssigmentException(BException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Impossible assign manager/admin"


class UnassignAnotherManagerException(BException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "You're not a manager of this user"
