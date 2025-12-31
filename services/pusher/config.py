from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    neo4j_uri: str = Field(..., alias="NEO4J_URI")
    neo4j_user: str = Field("neo4j", alias="NEO4J_USERNAME")
    neo4j_password: str = Field(..., alias="NEO4J_PASSWORD")

    host: str = Field("0.0.0.0", alias="HOST")
    port: int = Field(8001, alias="PORT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

settings = Settings()
