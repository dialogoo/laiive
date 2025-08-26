from typing import Dict
from pydantic_settings import BaseSettings, SettingsConfigDict


class ScraperSettings(BaseSettings):
    # Scrapy-ish knobs
    ROBOTSTXT_OBEY: bool = True
    USER_AGENT: str = "LaiiveCrawler/1.0"
    FROM: str = ""
    ACCEPT_LANGUAGE: str = "it,en;q=0.8"

    DOWNLOAD_DELAY: float = 1.0
    CONCURRENT_REQUESTS_PER_DOMAIN: int = 4

    AUTOTHROTTLE_ENABLED: bool = True
    AUTOTHROTTLE_START_DELAY: float = 0.5
    AUTOTHROTTLE_MAX_DELAY: float = 5.0

    HTTPCACHE_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=".env.dev",
        case_sensitive=False,
    )

    @property
    def default_headers(self) -> Dict[str, str]:
        headers = {
            "User-Agent": self.USER_AGENT,
            "Accept-Language": self.ACCEPT_LANGUAGE,
        }
        if self.FROM:
            headers["From"] = self.FROM
        return headers


settings = ScraperSettings()
