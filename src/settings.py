from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            Path(__file__).parent.parent.joinpath(".env"),
            Path(__file__).parent.parent.joinpath(".env.dev"),
            Path(__file__).parent.parent.joinpath(".env.test"),
        )
    )

    MODE: str
    LOG_LEVEL: str

    API_HOST: SecretStr
    API_PORT: SecretStr
    API_DSN: SecretStr

    DB_HOST: SecretStr
    DB_PORT: SecretStr
    DB_EXTERNAL_PORT: SecretStr
    DB_USER: SecretStr
    DB_PASSWORD: SecretStr
    DB_NAME: SecretStr
    DB_DSN: SecretStr

    JWT_ACCESS_KEY: SecretStr
    JWT_REFRESH_KEY: SecretStr
    JWT_ACCESS_TTL_MIN: int
    JWT_REFRESH_TTL_MIN: int
    JWT_ALGORITHM: str

    REDIS_HOST: SecretStr
    REDIS_PORT: SecretStr
    REDIS_URI: SecretStr


settings = Settings()
