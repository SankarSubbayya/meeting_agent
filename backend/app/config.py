from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "meeting-agents-api"
    debug: bool = False

    # Guild / internal callers must send this header to use tool routes
    internal_api_key: str = "dev-change-me"

    # SQLite durable store (override with postgres URL later)
    database_url: str = "sqlite+aiosqlite:///./meeting_agents.db"

    redis_url: str | None = "redis://localhost:6379/0"

    # Fireflies GraphQL API (https://docs.fireflies.ai)
    fireflies_api_key: str | None = None
    fireflies_graphql_url: str = "https://api.fireflies.ai/graphql"
    fireflies_timeout_seconds: float = 60.0

    # Guild.ai
    guild_api_base: str | None = None
    guild_api_key: str | None = None
    guild_workflow_meeting_path: str = "/v1/workflows/meeting-to-actions/run"

    # Google OAuth (user credentials for Gmail/Drive)
    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_refresh_token: str | None = None

    # WhatsApp Cloud API
    whatsapp_access_token: str | None = None
    whatsapp_phone_number_id: str | None = None
    whatsapp_api_version: str = "v21.0"

    # TinyFish
    tinyfish_api_key: str | None = None
    tinyfish_base_url: str = "https://api.tinyfish.ai"
    tinyfish_run_async_path: str = "/v1/run-async"

    # Cache / rate limits
    redis_cache_ttl_fireflies_seconds: int = 900
    redis_rate_limit_per_minute: int = 60


@lru_cache
def get_settings() -> Settings:
    return Settings()
