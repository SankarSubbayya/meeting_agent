from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from app.deps import DbSession, RedisDep, SettingsDep, correlation_id, verify_internal_key
from app.schemas import MeetingIngestRequest
from app.services.guild_client import trigger_meeting_workflow
from app.services.meeting_ingest import ingest_meeting

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.post("/ingest")
async def ingest(
    body: MeetingIngestRequest,
    _: Annotated[None, Depends(verify_internal_key)],
    session: DbSession,
    redis: RedisDep,
    settings: SettingsDep,
    corr: Annotated[str, Depends(correlation_id)],
) -> dict[str, Any]:
    if not settings.fireflies_api_key:
        raise HTTPException(status_code=503, detail="FIREFLIES_API_KEY not configured")
    meeting = await ingest_meeting(
        session=session,
        redis=redis,
        settings=settings,
        canonical_meeting_id=body.canonical_meeting_id,
        fireflies_transcript_id=body.fireflies_transcript_id,
        correlation_id=corr,
    )
    guild_resp: dict[str, Any] | None = None
    if body.trigger_guild:
        payload = {
            "correlation_id": corr,
            "meeting": {
                "id": meeting.id,
                "canonical_meeting_id": meeting.canonical_meeting_id,
                "source_used": meeting.source_used,
                "title": meeting.title,
                "summary": meeting.summary,
                "transcript_preview": (meeting.transcript or "")[:4000],
            },
        }
        guild_resp = await trigger_meeting_workflow(settings, payload)
        if guild_resp is None:
            guild_resp = {"skipped": True, "reason": "GUILD_API_BASE or GUILD_API_KEY not set"}

    return {
        "correlation_id": corr,
        "meeting_id": meeting.id,
        "canonical_meeting_id": meeting.canonical_meeting_id,
        "source_used": meeting.source_used,
        "guild": guild_resp,
    }
