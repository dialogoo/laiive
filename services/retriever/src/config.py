from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):

    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., alias="POSTGRES_DB")
    postgres_host: str = Field("db", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")
    postgres_url: str = Field(..., alias="POSTGRES_URL")

    openai_api_key: str | None = Field(None, alias="OPENAI_API_KEY")
    model_base: str = Field(..., alias="MODEL_BASE")
    model_test: str = Field(..., alias="MODEL_TEST")

    api_url: str = Field(..., alias="API_URL")
    host: str = Field(..., alias="HOST")
    port: int = Field(..., alias="PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
