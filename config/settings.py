import os
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = os.getenv("ENV", "dev")


class Settings(BaseSettings):
    database_url: str
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_echo: bool = False
    env: str = ENV

    model_config = SettingsConfigDict(
        env_file=".env" if ENV == "dev" else None,
        env_file_encoding="utf-8",
    )


def get_settings():
    return Settings()

settings = get_settings()
