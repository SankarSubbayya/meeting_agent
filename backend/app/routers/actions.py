import asyncio
import base64
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from app.db.models import AuditLog
from app.deps import DbSession, RedisDep, SettingsDep, correlation_id, parse_capabilities, require_capability, verify_internal_key
from app.schemas import DriveFileRequest, GmailSendRequest, TinyFishRunRequest, WhatsAppSendRequest
from app.services.google_clients import drive_download_media_sync, drive_get_file_metadata_sync, gmail_send_message
from app.services.tinyfish_client import start_tinyfish_run
from app.services.whatsapp_policy import WhatsAppPolicyError, send_whatsapp_message

router = APIRouter(prefix="/tools/actions", tags=["action-tools"])


@router.post("/gmail/send")
async def gmail_send(
    body: GmailSendRequest,
    _: Annotated[None, Depends(verify_internal_key)],
    session: DbSession,
    settings: SettingsDep,
    caps: Annotated[set[str], Depends(parse_capabilities)],
    corr: Annotated[str, Depends(correlation_id)],
) -> dict[str, Any]:
    require_capability("gmail:send", caps)
    att: bytes | None = None
    if body.attachment_base64:
        try:
            att = base64.b64decode(body.attachment_base64)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid attachment_base64") from e

    try:
        result = await asyncio.to_thread(
            gmail_send_message,
            settings,
            to=body.to,
            subject=body.subject,
            body_text=body.body_text,
            attachment_name=body.attachment_name,
            attachment_bytes=att,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e

    session.add(
        AuditLog(
            meeting_id=None,
            correlation_id=corr,
            tool_name="gmail_send",
            channel="action",
            detail_json={"to": body.to, "subject": body.subject},
        )
    )
    await session.commit()
    return {"result": result}


@router.post("/drive/file")
async def drive_file_metadata(
    body: DriveFileRequest,
    _: Annotated[None, Depends(verify_internal_key)],
    settings: SettingsDep,
    caps: Annotated[set[str], Depends(parse_capabilities)],
) -> dict[str, Any]:
    require_capability("drive:read", caps)
    try:
        meta = await asyncio.to_thread(drive_get_file_metadata_sync, settings, body.file_id)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    return {"metadata": meta}


@router.post("/drive/download")
async def drive_download(
    body: DriveFileRequest,
    _: Annotated[None, Depends(verify_internal_key)],
    settings: SettingsDep,
    caps: Annotated[set[str], Depends(parse_capabilities)],
) -> dict[str, Any]:
    require_capability("drive:read", caps)
    try:
        content, ctype = await asyncio.to_thread(drive_download_media_sync, settings, body.file_id)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    import base64 as b64

    return {"content_type": ctype, "content_base64": b64.b64encode(content).decode("ascii")}


@router.post("/whatsapp/send")
async def whatsapp_send(
    body: WhatsAppSendRequest,
    _: Annotated[None, Depends(verify_internal_key)],
    session: DbSession,
    settings: SettingsDep,
    redis: RedisDep,
    caps: Annotated[set[str], Depends(parse_capabilities)],
    corr: Annotated[str, Depends(correlation_id)],
) -> dict[str, Any]:
    require_capability("whatsapp:send", caps)
    payload = body.model_dump()
    try:
        result = await send_whatsapp_message(settings, redis, payload)
    except WhatsAppPolicyError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e

    session.add(
        AuditLog(
            meeting_id=None,
            correlation_id=corr,
            tool_name="whatsapp_send",
            channel="action",
            detail_json={"to": body.to, "kind": body.kind},
        )
    )
    await session.commit()
    return {"result": result}


@router.post("/tinyfish/run")
async def tinyfish_run(
    body: TinyFishRunRequest,
    _: Annotated[None, Depends(verify_internal_key)],
    session: DbSession,
    settings: SettingsDep,
    redis: RedisDep,
    caps: Annotated[set[str], Depends(parse_capabilities)],
    corr: Annotated[str, Depends(correlation_id)],
) -> dict[str, Any]:
    require_capability("tinyfish:run", caps)
    try:
        job = await start_tinyfish_run(
            settings,
            session,
            redis,
            goal=body.goal,
            meeting_id=body.meeting_id,
            extra=body.extra,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e

    session.add(
        AuditLog(
            meeting_id=body.meeting_id,
            correlation_id=corr,
            tool_name="tinyfish_run",
            channel="action",
            detail_json={"job_db_id": job.id, "external_job_id": job.external_job_id},
        )
    )
    await session.commit()
    return {"job_id": job.id, "external_job_id": job.external_job_id, "status": job.status}
