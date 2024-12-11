from fastapi import APIRouter, status

from src.entities.auth.dependencies import AuthServiceObj
from src.entities.auth.schemas import JWTLoginResponseSchema, RefreshTokenSchema
from src.entities.user.dependencies import UserServiceObj
from src.entities.user.schemas import UserLoginSchema

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@auth_router.post(
    path="/login",
    response_model=JWTLoginResponseSchema,
    status_code=status.HTTP_200_OK
)
async def login(user_service: UserServiceObj, login_schema: UserLoginSchema):
    return await user_service.login(login_schema)


@auth_router.post(
    path="/refresh",
    response_model=JWTLoginResponseSchema,
    status_code=status.HTTP_200_OK
)
async def refresh_token(auth_service: AuthServiceObj, refresh_schema: RefreshTokenSchema):
    return await auth_service.refresh_token(refresh_schema.refresh_token)
