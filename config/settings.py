import os
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = os.getenv("ENV", "dev")

class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env" if ENV == "dev" else None
    )

def get_settings():
    return Settings()
