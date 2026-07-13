"""
Application configuration loaded from environment variables.
Uses pydantic-settings for validation and IDE-friendly typing.
"""
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Runtime configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---- API ----
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    api_title: str = "DevCraft Studio API"
    api_version: str = "1.0.0"
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])

    # ---- Database ----
    database_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/dev.db"

    # ---- Integrations ----
    bot_notify_url: str = ""        # if set, leads are forwarded here (Telegram bot webhook)
    bot_notify_timeout: float = 5.0

    # ---- Security ----
    admin_token: str = "change-me-in-prod"
    rate_limit_per_minute: int = 30

    # ---- Static / SPA ----
    site_dir: Path = BASE_DIR.parent / "site"
    serve_site: bool = True


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings accessor."""
    return Settings()
