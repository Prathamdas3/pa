"""Application configuration.

Loads and validates settings from environment variables using pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv
from functools import lru_cache
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parents[1]
TEMP_DIR = BASE_DIR / "temp"


class Settings(BaseSettings):
    env: str = Field(validation_alias="ENV", default="development")
    debug: bool = Field(validation_alias="DEBUG", default=False)
    database_url: str = Field(validation_alias="DATABASE_URL", default="")
    access_token_expire_minutes: int = Field(
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES", default=30
    )
    refresh_token_expire_days: int = Field(
        validation_alias="REFRESH_TOKEN_EXPIRE_DAYS", default=7
    )
    secret_key: str = Field(validation_alias="SECRET_KEY", default="")
    algorithm: str = Field(validation_alias="ALGORITHM", default="HS256")
    frontend_url: str = Field(
        validation_alias="FRONTEND_URL", default="http://localhost:3000"
    )
    backend_url: str = Field(
        validation_alias="BACKEND_URL", default="http://localhost:9000"
    )

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_config() -> Settings:
    """Get cached application settings instance.

    Returns:
        Cached Settings instance.
    """
    return Settings()


config = get_config()