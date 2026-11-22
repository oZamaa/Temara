from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, read from JOBTRACK_* environment variables."""

    model_config = SettingsConfigDict(env_prefix="JOBTRACK_")

    data_dir: Path = Path("/data")
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
