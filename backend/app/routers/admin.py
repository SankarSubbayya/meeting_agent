from typing import Annotated

from fastapi import APIRouter, Depends

from app.deps import RedisDep, verify_internal_key

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/whatsapp/opt-in/{wa_id}")
async def whatsapp_opt_in(
    wa_id: str,
    _: Annotated[None, Depends(verify_internal_key)],
    redis: RedisDep,
) -> dict:
    """Mark a WhatsApp user (digits only) as opted in for outbound messages."""
    if redis is None:
        return {"ok": False, "detail": "Redis not configured"}
    clean = "".join(c for c in wa_id if c.isdigit())
    await redis.set(f"whatsapp:optin:{clean}", "1", ex=86400 * 365)
    return {"ok": True, "wa_id": clean}
