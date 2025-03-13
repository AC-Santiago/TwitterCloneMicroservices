from pathlib import Path
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings
from functools import lru_cache


def find_root_path() -> Path:
    current = Path(__file__).resolve().parent
    root = current.parent.parent.parent
    if (root / ".env").exists():
        return root
    return current


ROOT_DIR = find_root_path()


class Settings(BaseSettings):
    # Service URLs
    AUTH_SERVICE_URL: str = "http://localhost:8000"
    TWEETS_SERVICE_URL: str = "http://localhost:8001"
    INTERACTIONS_SERVICE_URL: str = "http://localhost:8002"

    # HTTP Client settings
    HTTP_TIMEOUT: float = 30.0

    def to_dict(self) -> dict:
        return self.model_dump()

    class Config:
        env_file = [str(ROOT_DIR / ".env"), ".env"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


SettingsDepends = Annotated[Settings, Depends(get_settings)]
