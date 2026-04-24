"""TinyFish async run — store job id in DB + Redis."""

from __future__ import annotations

from typing import Any

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.db.models import TinyFishJob
from app.services.redis_service import tinyfish_job_pointer


async def start_tinyfish_run(
    settings: Settings,
    session: AsyncSession,
    redis,
    *,
    goal: str,
    meeting_id: str | None,
    extra: dict[str, Any] | None = None,
) -> TinyFishJob:
    if not settings.tinyfish_api_key:
        raise RuntimeError("TinyFish API key not configured")
    url = settings.tinyfish_base_url.rstrip("/") + settings.tinyfish_run_async_path
    headers = {
        "Authorization": f"Bearer {settings.tinyfish_api_key}",
        "Content-Type": "application/json",
    }
    payload = {"goal": goal, **(extra or {})}
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json() if r.content else {}
    ext_id = str(data.get("job_id") or data.get("id") or data.get("run_id") or "")
    if not ext_id:
        ext_id = r.headers.get("X-Job-Id", "unknown")

    job = TinyFishJob(external_job_id=ext_id, meeting_id=meeting_id, status="submitted", goal=goal)
    session.add(job)
    await session.commit()
    await session.refresh(job)
    await tinyfish_job_pointer(redis, ext_id, meeting_id)
    return job
