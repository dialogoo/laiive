from pydantic import BaseSettings, Field, PostgresDsn, validator
from functools import lru_cache

class Settings(BaseSettings):


    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., alias="POSTGRES_DB")
    postgres_host: str = Field("db", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")
    postgres_url: str = Field(..., alias="POSTGRES_URL")

    openai_api_key: str | None = Field(None, alias="OPENAI_API_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:  # singleton
    return Settings()
