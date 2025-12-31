from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., alias="POSTGRES_DB")
    postgres_host: str = Field("db", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")
    postgres_url: str = Field(..., alias="POSTGRES_URL")

    llm_provider: Literal["openai", "anthropic", "gemini", "ollama"] = Field(
        "openai", alias="LLM_PROVIDER"
    )
    llm_model: str = Field("gpt-3.5-turbo", alias="LLM_MODEL")
    llm_temperature: float = Field(0.1, alias="LLM_TEMPERATURE")

    openai_api_key: str | None = Field(None, alias="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(None, alias="ANTHROPIC_API_KEY")
    gemini_api_key: str | None = Field(None, alias="GEMINI_API_KEY")
    ollama_base_url: str = Field("http://localhost:11434", alias="OLLAMA_BASE_URL")

    api_url: str = Field(..., alias="API_URL")
    host: str = Field(..., alias="HOST")
    port: int = Field(..., alias="PORT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
