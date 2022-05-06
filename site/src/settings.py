from enum import Enum

from db.settings import DatabaseSettings
from apps.example.settings import ExampleSettings


class Settings(DatabaseSettings, ExampleSettings):
    class EnvMode(Enum):
        prod = "PROD"
        dev = "DEV"

    ENV: EnvMode = EnvMode.dev

    @property
    def is_production(self):
        return self.ENV == self.EnvMode.prod

    # Настройки сервера
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    SERVER_DOMAIN: str = "http://localhost"
    LOGGING_LEVEL: str = "INFO"

    # Настройки проекта
    PROJECT_NAME: str = "FastAPI"
    VERSION: str = "1.0.0"

    class Config:
        # for local development without docker
        # broken source .env
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
