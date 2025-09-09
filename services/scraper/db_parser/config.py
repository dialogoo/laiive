from pydantic_settings import BaseSettings, SettingsConfigDict


class db_parser_settings(BaseSettings):

    POSTGRES_URL: str

    model_config = SettingsConfigDict(
        env_file="../../.env",
        case_sensitive=False,
        extra="ignore",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Fix the URL format for psycopg2
        if self.POSTGRES_URL.startswith("postgresql+asyncpg://"):
            self.POSTGRES_URL = self.POSTGRES_URL.replace(
                "postgresql+asyncpg://", "postgresql://"
            )


settings = db_parser_settings()
