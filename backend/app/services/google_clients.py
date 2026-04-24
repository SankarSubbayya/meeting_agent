"""Gmail send + Drive read using OAuth refresh token (sync; call via asyncio.to_thread)."""

from __future__ import annotations

import base64
from email.message import EmailMessage
from typing import Any

import httpx
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.config import Settings


def _creds(settings: Settings) -> Credentials:
    if not settings.google_client_id or not settings.google_client_secret or not settings.google_refresh_token:
        raise RuntimeError("Google OAuth not configured (client id/secret/refresh token)")
    return Credentials(
        token=None,
        refresh_token=settings.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        scopes=[
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/drive.readonly",
        ],
    )


def _ensure_token(creds: Credentials) -> None:
    if not creds.valid:
        creds.refresh(Request())


def gmail_send_message(
    settings: Settings,
    *,
    to: str,
    subject: str,
    body_text: str,
    attachment_name: str | None = None,
    attachment_bytes: bytes | None = None,
) -> dict[str, Any]:
    creds = _creds(settings)
    _ensure_token(creds)
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)

    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body_text)
    if attachment_name and attachment_bytes:
        msg.add_attachment(attachment_bytes, maintype="application", subtype="octet-stream", filename=attachment_name)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    try:
        sent = service.users().messages().send(userId="me", body={"raw": raw}).execute()
        return {"id": sent.get("id"), "threadId": sent.get("threadId")}
    except HttpError as e:
        raise RuntimeError(f"Gmail API error: {e}") from e


def drive_get_file_metadata_sync(settings: Settings, file_id: str) -> dict[str, Any]:
    creds = _creds(settings)
    _ensure_token(creds)
    service = build("drive", "v3", credentials=creds, cache_discovery=False)
    try:
        return service.files().get(fileId=file_id, fields="id,name,mimeType,size").execute()
    except HttpError as e:
        raise RuntimeError(f"Drive API error: {e}") from e


def drive_download_media_sync(settings: Settings, file_id: str) -> tuple[bytes, str | None]:
    creds = _creds(settings)
    _ensure_token(creds)
    token = creds.token
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    with httpx.Client(timeout=120.0) as client:
        r = client.get(url, headers={"Authorization": f"Bearer {token}"})
        r.raise_for_status()
        return r.content, r.headers.get("content-type")
