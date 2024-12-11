import sys
from pathlib import Path

import sentry_sdk
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.entities.auth.router import auth_router
from src.entities.message.router import message_router
from src.entities.role.router import role_router
from src.entities.user.router import user_router
from src.settings import settings

sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI

if settings.MODE != "TEST":
    # Result example - https://prnt.sc/C8hoRsFHZi1E
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN.get_secret_value(),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=settings.SENTRY_RATE,
        _experiments={
            # Set continuous_profiling_auto_start to True
            # to automatically start the profiler on when
            # possible.
            "continuous_profiling_auto_start": True,
        },
    )
app = FastAPI(
    title="Test task",
    summary="Just a test task",
    description="Just a test task",
)

app.include_router(auth_router)
app.include_router(role_router)
app.include_router(user_router)
app.include_router(message_router)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(settings.REDIS_URI)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
