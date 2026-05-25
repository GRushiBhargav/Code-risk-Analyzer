from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    GITHUB_WEBHOOK_SECRET: str
    DATABASE_URL: str
    GITHUB_TOKEN: str

    class Config:
        env_file = BASE_DIR / ".env"


settings = Settings()
