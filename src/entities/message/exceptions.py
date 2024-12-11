from fastapi import status

from src.entities.base_exception import BException


class MessageNotFound(BException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Message not found"
