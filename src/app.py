import sys
from pathlib import Path

from src.entities.auth.router import auth_router
from src.entities.message.router import message_router
from src.entities.role.router import role_router
from src.entities.user.router import user_router

sys.path.append(str(Path(__file__).parent))


from fastapi import FastAPI

app = FastAPI(
    title="Test task",
    summary="Just a test task",
    description="Just a test task",
)

app.include_router(auth_router)
app.include_router(role_router)
app.include_router(user_router)
app.include_router(message_router)
