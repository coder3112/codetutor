import os
from enum import Enum
from pathlib import Path

from pydantic import BaseSettings

testing = os.getenv("TEST")
env_file_path = Path(__file__).absolute().parent.parent.with_name(".env")
if testing:
    env_file_path = Path(__file__).absolute().parent.parent.with_name(".env.testing")


class AppMode(Enum):
    DEV = "development"
    PROD = "production"


class Settings(BaseSettings):
    fastapi_env: AppMode = AppMode.DEV
    name: str
    secret_key: str
    algorithm: str
    # Postgres connection settings
    postgres_db: str
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str

    # API Keys
    vimeo_token: str
    vimeo_client_id: str
    vimeo_client_secret: str

    class Config:
        env_file = env_file_path

    @property
    def is_dev(self) -> bool:
        return self.fastapi_env == AppMode.DEV


settings = Settings()
