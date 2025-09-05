from pydantic_settings import BaseSettings, SettingsConfigDict


class ScraperSettings(BaseSettings):
    ROBOTSTXT_OBEY: bool
    USER_AGENT: str
    # FROM: str
    ACCEPT_LANGUAGE: str
    CONCURRENT_REQUESTS_PER_DOMAIN: int = 4
    AUTOTHROTTLE_ENABLED: bool = True
    AUTOTHROTTLE_START_DELAY: float = 0.5
    AUTOTHROTTLE_MAX_DELAY: float = 5.0
    DOWNLOAD_TIMEOUT: int = 30
    RETRY_TIMES: int = 2
    RETRY_HTTP_CODES: list[int]
    HTTPCACHE_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file="../.env.dev",
        case_sensitive=False,
        extra="ignore",
    )


settings = ScraperSettings()
