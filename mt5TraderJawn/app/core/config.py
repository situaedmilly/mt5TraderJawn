from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./dev.db"
    database_echo: bool = False

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    environment: str = "development"
    secret_key: str = "change-me"

    mt5_host: str | None = None
    mt5_port: int | None = None
    mt5_login: str | None = None
    mt5_password: str | None = None
    mt5_server: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
