""" Настройки базы данных и редиса """
from typing import Any

import pytz
from pydantic import BaseSettings, validator, PostgresDsn


class DatabaseSettings(BaseSettings):
    """Настройки базы данных"""

    # Настройки базы
    POSTGRES_HOST: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str
    POSTGRES_URI: PostgresDsn = None

    @validator("POSTGRES_URI")
    def assemble_database_url(
        cls,
        _,
        values: dict[str, Any],
    ) -> str:
        return PostgresDsn.build(
            scheme="postgres",
            host=values["POSTGRES_HOST"],
            port=values["POSTGRES_PORT"],
            user=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"],
            path=f'/{values["POSTGRES_DB"]}',
        )

    TORTOISE_ORM: dict = {}

    @validator("TORTOISE_ORM")
    def assemble_orm(cls, _, values: dict[str, Any]) -> dict:
        """Настройки tortoise"""
        return dict(
            connections=dict(
                default=values["POSTGRES_URI"],
            ),
            apps=dict(
                models=dict(
                    models=["apps.models"],
                    default_connection="default",
                )
            ),
            use_tz=False,
            timezone=pytz.UTC.zone,
        )
