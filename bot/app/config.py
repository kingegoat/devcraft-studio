"""Bot configuration loaded from environment variables."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # devcraft-studio/


class Settings(BaseSettings):
    """Runtime configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---- Bot ----
    bot_token: str = ""                    # required in production
    bot_mode: str = "polling"              # polling | webhook
    webhook_url: str = ""                  # e.g. https://api.example.com/bot/webhook
    webhook_path: str = "/bot/webhook"
    webhook_secret: str = ""

    # ---- API ----
    api_base_url: str = "http://localhost:8000"
    api_admin_token: str = ""

    # ---- Admin notifications ----
    admin_chat_ids: str = ""               # comma-separated
    internal_notify_token: str = ""        # shared secret with API

    # ---- Server ----
    bot_host: str = "0.0.0.0"
    bot_port: int = 8080

    @property
    def admin_ids(self) -> list[int]:
        return [int(x) for x in self.admin_chat_ids.split(",") if x.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
