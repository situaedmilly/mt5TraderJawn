from functools import lru_cache
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    """Application settings"""
    # Database
    database_url: PostgresDsn
    database_echo: bool = False
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    # Environment
    environment: str = "development"
    # Security
    secret_key: str = "change-this-in-production"
    # MT5 bridge connection
    mt5_host: str | None = None
    mt5_port: int | None = None
    mt5_login: int | None = None
    mt5_password: str | None = None
    mt5_server: str | None = None
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
