"""Meeting ingest from Fireflies GraphQL API; persist Meeting + idempotency."""

from __future__ import annotations

import json
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.db.models import AuditLog, Meeting
from app.services.fireflies_client import FirefliesAPIError, FirefliesClient
from app.services.redis_service import is_processed, mark_processed


def _extract_text_from_ingest_result(result: Any) -> str:
    if result is None:
        return ""
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        t = result.get("transcript")
        if isinstance(t, str):
            return t
        if "text" in result and isinstance(result["text"], str):
            return result["text"]
        try:
            return json.dumps(result)[:500_000]
        except Exception:
            return str(result)
    return str(result)


def _extract_summary_title(result: Any) -> tuple[str | None, str | None]:
    if not isinstance(result, dict):
        return None, None
    summary = result.get("summary") if isinstance(result.get("summary"), str) else None
    title = result.get("title") if isinstance(result.get("title"), str) else None
    return summary, title


def _usable_transcript(text: str) -> bool:
    return len(text.strip()) >= 40


async def ingest_meeting(
    *,
    session: AsyncSession,
    redis,
    settings: Settings,
    canonical_meeting_id: str,
    fireflies_transcript_id: str,
    correlation_id: str,
) -> Meeting:
    dedupe_key = f"processed:meeting:{canonical_meeting_id}"
    if await is_processed(redis, dedupe_key):
        res = await session.execute(
            select(Meeting)
            .where(Meeting.canonical_meeting_id == canonical_meeting_id)
            .order_by(Meeting.created_at.desc())
            .limit(1)
        )
        existing = res.scalar_one_or_none()
        if existing:
            return existing

    client = FirefliesClient(settings)
    source_used = "fireflies"
    raw: Any = None
    transcript = ""
    summary: str | None = None
    title: str | None = None

    try:
        raw = await client.fetch_transcript(fireflies_transcript_id)
        transcript = _extract_text_from_ingest_result(raw)
        summary, title = _extract_summary_title(raw)
    except (FirefliesAPIError, httpx.HTTPError, OSError) as e:
        raw = {"error": str(e), "transcript_id": fireflies_transcript_id}

    meeting = Meeting(
        canonical_meeting_id=canonical_meeting_id,
        source_used=source_used,
        title=title,
        transcript=transcript or None,
        summary=summary,
        raw_mcp_payload=raw if isinstance(raw, dict) else {"raw": raw},
    )
    session.add(meeting)
    await session.flush()
    session.add(
        AuditLog(
            meeting_id=meeting.id,
            correlation_id=correlation_id,
            tool_name="ingest_meeting",
            channel="read",
            detail_json={
                "canonical_meeting_id": canonical_meeting_id,
                "source_used": source_used,
                "fireflies_transcript_id": fireflies_transcript_id,
                "transcript_ok": _usable_transcript(transcript),
            },
        ),
    )
    await session.commit()
    await session.refresh(meeting)
    await mark_processed(redis, dedupe_key)
    return meeting
