from pydantic_settings import BaseSettings, SettingsConfigDict


class db_parser_settings(BaseSettings):

    POSTGRES_URL: str

    model_config = SettingsConfigDict(
        env_file="../../.env",
        case_sensitive=False,
        extra="ignore",
    )


settings = db_parser_settings()
