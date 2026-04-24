# Backend scaffold (copy into `backend/` when Agent mode is on)

Until Agent mode is enabled, create these files manually or paste from below.

## Layout

```text
backend/
  requirements.txt
  app/
    __init__.py
    config.py
    main.py
    routers/
      __init__.py
      read_tools.py
      actions.py
    services/
      __init__.py
      meeting_fetch.py
      redis_client.py
```

## `backend/requirements.txt`

```text
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
pydantic-settings>=2.6.0
httpx>=0.27.0
redis>=5.2.0
```

## `backend/app/config.py`

```python
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "meeting-agents-api"
    debug: bool = False

    redis_url: str | None = None

    fireflies_api_key: str | None = None
    fireflies_graphql_url: str = "https://api.fireflies.ai/graphql"

    guild_api_base: str | None = None
    guild_api_key: str | None = None

    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_refresh_token: str | None = None

    whatsapp_access_token: str | None = None
    whatsapp_phone_number_id: str | None = None
    whatsapp_business_account_id: str | None = None

    tinyfish_api_key: str | None = None
    tinyfish_base_url: str = "https://api.tinyfish.ai"

    openai_api_key: str | None = None
    anthropic_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

## `backend/app/services/redis_client.py`

```python
from redis.asyncio import Redis

from app.config import get_settings


async def get_redis() -> Redis | None:
    url = get_settings().redis_url
    if not url:
        return None
    return Redis.from_url(url, decode_responses=True)
```

## `backend/app/services/meeting_fetch.py`

```python
"""Fetch transcript via Fireflies GraphQL (`transcript` query)."""

from dataclasses import dataclass
from typing import Any


@dataclass
class MeetingPayload:
    canonical_meeting_id: str
    source_used: str  # "fireflies"
    raw: dict[str, Any]


async def fetch_meeting_transcript(
    *,
    canonical_meeting_id: str,
    transcript_id: str,
    fetch_fireflies_transcript: Any,
) -> MeetingPayload:
    """
    fetch_fireflies_transcript: async (transcript_id: str) -> dict
    """
    raw = await fetch_fireflies_transcript(transcript_id)
    return MeetingPayload(canonical_meeting_id, "fireflies", raw)


def _usable_transcript(raw: dict) -> bool:
    text = str(raw.get("transcript") or raw.get("text") or "")
    return len(text.strip()) > 0
```

## `backend/app/routers/read_tools.py`

```python
from fastapi import APIRouter, Depends

from app.config import Settings, get_settings

router = APIRouter(prefix="/tools/read", tags=["read"])


@router.post("/fireflies/transcript")
async def fireflies_transcript(body: dict, settings: Settings = Depends(get_settings)):
    """Call Fireflies GraphQL with settings.fireflies_api_key."""
    _ = settings
    return {"status": "stub", "body": body}
```

## `backend/app/routers/actions.py`

```python
from fastapi import APIRouter, Depends

from app.config import Settings, get_settings

router = APIRouter(prefix="/tools/actions", tags=["actions"])


@router.post("/gmail/send")
async def gmail_send(body: dict, settings: Settings = Depends(get_settings)):
    _ = settings
    return {"status": "stub", "body": body}


@router.post("/whatsapp/send")
async def whatsapp_send(body: dict, settings: Settings = Depends(get_settings)):
    _ = settings
    return {"status": "stub", "body": body}


@router.post("/tinyfish/run")
async def tinyfish_run(body: dict, settings: Settings = Depends(get_settings)):
    _ = settings
    return {"status": "stub", "body": body}
```

## `backend/app/main.py`

```python
from fastapi import FastAPI

from app.routers import actions, read_tools

app = FastAPI(title="Meeting Agents API")
app.include_router(read_tools.router)
app.include_router(actions.router)


@app.get("/health")
def health():
    return {"status": "ok"}
```

## `backend/app/routers/__init__.py`

(empty file)

## Run

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Guild should call `https://<your-host>/tools/read/*` and `/tools/actions/*` with your auth (add API key middleware next).
