"""Redis: idempotency, cache, simple rate limits."""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

import redis.asyncio as redis


async def dedupe_once(
    r: redis.Redis | None,
    key: str,
    ttl_seconds: int = 86400,
) -> bool:
    """
    Returns True if this is the first time seeing the key (set OK).
    Returns False if key already existed (duplicate).
    """
    if r is None:
        return True
    ok = await r.set(key, "1", nx=True, ex=ttl_seconds)
    return bool(ok)


async def is_processed(r: redis.Redis | None, key: str) -> bool:
    if r is None:
        return False
    v = await r.get(key)
    return v == "1"


async def mark_processed(r: redis.Redis | None, key: str, ttl_seconds: int = 86400 * 30) -> None:
    if r is None:
        return
    await r.set(key, "1", ex=ttl_seconds)


async def cache_get_json(r: redis.Redis | None, key: str) -> Any | None:
    if r is None:
        return None
    raw = await r.get(key)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


async def cache_set_json(
    r: redis.Redis | None,
    key: str,
    value: Any,
    ttl_seconds: int,
) -> None:
    if r is None:
        return
    await r.set(key, json.dumps(value), ex=ttl_seconds)


def fireflies_transcript_cache_key(transcript_id: str) -> str:
    h = hashlib.sha256(transcript_id.encode()).hexdigest()[:48]
    return f"tool:fireflies:transcript:{h}"


async def rate_limit_allow(
    r: redis.Redis | None,
    *,
    scope: str,
    identity: str,
    limit_per_minute: int,
) -> bool:
    if r is None:
        return True
    window = int(time.time()) // 60
    key = f"rl:{scope}:{identity}:{window}"
    n = await r.incr(key)
    if n == 1:
        await r.expire(key, 70)
    return n <= limit_per_minute


async def tinyfish_job_pointer(
    r: redis.Redis | None,
    job_id: str,
    meeting_id: str | None,
) -> None:
    if r is None:
        return
    await r.set(f"tinyfish:job:{job_id}", json.dumps({"meeting_id": meeting_id}), ex=86400 * 7)
