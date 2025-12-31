from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    api_url: str = Field("http://localhost:8000", alias="API_URL")
    api_path: str = Field("/chat", alias="API_PATH")

    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
