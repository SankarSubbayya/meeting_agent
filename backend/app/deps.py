from collections.abc import AsyncGenerator
from typing import Annotated
from uuid import uuid4

import redis.asyncio as redis
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.db.session import get_session


async def get_redis_dep(settings: Annotated[Settings, Depends(get_settings)]) -> AsyncGenerator[redis.Redis | None, None]:
    if not settings.redis_url:
        yield None
        return
    client = redis.from_url(settings.redis_url, decode_responses=True)
    try:
        yield client
    finally:
        await client.aclose()


def verify_internal_key(
    settings: Annotated[Settings, Depends(get_settings)],
    x_api_key: Annotated[str | None, Header(alias="X-Internal-API-Key")] = None,
) -> None:
    if not x_api_key or x_api_key != settings.internal_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing X-Internal-API-Key")


def correlation_id(
    x_correlation_id: Annotated[str | None, Header(alias="X-Correlation-Id")] = None,
) -> str:
    return x_correlation_id or str(uuid4())


def parse_capabilities(
    x_capabilities: Annotated[str | None, Header(alias="X-Agent-Capabilities")] = None,
) -> set[str]:
    if not x_capabilities:
        return set()
    return {c.strip() for c in x_capabilities.split(",") if c.strip()}


def require_capability(cap: str, caps: Annotated[set[str], Depends(parse_capabilities)]) -> None:
    """If client sends capabilities header, cap must be listed. If header omitted, allow (dev)."""
    if not caps:
        return
    if cap not in caps:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing capability: {cap}",
        )


DbSession = Annotated[AsyncSession, Depends(get_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
RedisDep = Annotated[redis.Redis | None, Depends(get_redis_dep)]
