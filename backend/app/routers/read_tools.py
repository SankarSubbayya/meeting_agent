from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from app.db.models import AuditLog
from app.deps import (
    DbSession,
    RedisDep,
    SettingsDep,
    correlation_id,
    parse_capabilities,
    require_capability,
    verify_internal_key,
)
from app.schemas import FirefliesTranscriptRequest
from app.services.fireflies_client import FirefliesAPIError, FirefliesClient
from app.services.redis_service import cache_get_json, cache_set_json, fireflies_transcript_cache_key, rate_limit_allow

router = APIRouter(prefix="/tools/read", tags=["read-tools"])


@router.post("/fireflies/transcript")
async def fireflies_transcript(
    body: FirefliesTranscriptRequest,
    _: Annotated[None, Depends(verify_internal_key)],
    session: DbSession,
    redis: RedisDep,
    settings: SettingsDep,
    caps: Annotated[set[str], Depends(parse_capabilities)],
    corr: Annotated[str, Depends(correlation_id)],
) -> dict[str, Any]:
    require_capability("fireflies:transcript", caps)
    if not settings.fireflies_api_key:
        raise HTTPException(status_code=503, detail="FIREFLIES_API_KEY not configured")
    if not await rate_limit_allow(redis, scope="fireflies", identity="global", limit_per_minute=settings.redis_rate_limit_per_minute):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    cache_key = fireflies_transcript_cache_key(body.transcript_id)
    cached = await cache_get_json(redis, cache_key)
    if cached is not None:
        return {"cached": True, "result": cached}

    client = FirefliesClient(settings)
    try:
        result = await client.fetch_transcript(body.transcript_id)
    except FirefliesAPIError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e

    await cache_set_json(redis, cache_key, result, ttl_seconds=settings.redis_cache_ttl_fireflies_seconds)
    session.add(
        AuditLog(
            meeting_id=None,
            correlation_id=corr,
            tool_name="fireflies_transcript",
            channel="read",
            detail_json={"transcript_id": body.transcript_id[:128]},
        )
    )
    await session.commit()
    return {"cached": False, "result": result}
