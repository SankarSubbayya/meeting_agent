from typing import Any

from pydantic import BaseModel, Field


class FirefliesTranscriptRequest(BaseModel):
    transcript_id: str = Field(..., min_length=1, max_length=256)


class MeetingIngestRequest(BaseModel):
    canonical_meeting_id: str = Field(..., min_length=1, max_length=512)
    fireflies_transcript_id: str = Field(..., min_length=1, max_length=256)
    trigger_guild: bool = True


class GmailSendRequest(BaseModel):
    to: str
    subject: str
    body_text: str
    attachment_name: str | None = None
    attachment_base64: str | None = None


class WhatsAppSendRequest(BaseModel):
    to: str
    kind: str  # template | session
    template_name: str | None = None
    language_code: str | None = None
    template_components: list[dict[str, Any]] | None = None
    text: str | None = None
    preview_url: bool = False
    session_active: bool = False


class TinyFishRunRequest(BaseModel):
    goal: str = Field(..., min_length=1, max_length=16_000)
    meeting_id: str | None = None
    extra: dict[str, Any] | None = None


class DriveFileRequest(BaseModel):
    file_id: str


class WhatsAppOptInRequest(BaseModel):
    """Set opt-in for a WhatsApp user id (digits, no +)."""

    wa_id: str
