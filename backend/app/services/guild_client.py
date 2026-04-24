"""Trigger Guild.ai workflows after a meeting is ingested (HTTP stub — paths vary by Guild product)."""

from __future__ import annotations

from typing import Any

import httpx

from app.config import Settings


async def trigger_meeting_workflow(settings: Settings, payload: dict[str, Any]) -> dict[str, Any] | None:
    if not settings.guild_api_base or not settings.guild_api_key:
        return None
    base = settings.guild_api_base.rstrip("/")
    path = settings.guild_workflow_meeting_path
    url = f"{base}{path}"
    headers = {
        "Authorization": f"Bearer {settings.guild_api_key}",
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(url, json=payload, headers=headers)
            r.raise_for_status()
            if r.content:
                return r.json()
        return {}
    except httpx.HTTPError as e:
        status: int | None = None
        if isinstance(e, httpx.HTTPStatusError):
            status = e.response.status_code
        return {"error": str(e), "status_code": status}
