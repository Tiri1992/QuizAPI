from pydantic import BaseSettings
from pydantic import PostgresDsn
from functools import lru_cache


class Settings(BaseSettings):

    api_v1: str = "/api/v1"

    postgres_uri: PostgresDsn

    class Config:
        env_file = ".env"
        env_file_enconding = "utf-8"


@lru_cache
def load_settings() -> Settings:
    return Settings()


settings = load_settings()
