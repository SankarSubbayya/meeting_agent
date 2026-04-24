"""
WhatsApp Cloud API helpers with basic policy:
- template messages for cold / outside 24h session
- session messages only when session_active and within business rules (caller must attest)
"""

from __future__ import annotations

from typing import Any

import httpx

from app.config import Settings


class WhatsAppPolicyError(ValueError):
    pass


def validate_outbound_request(body: dict[str, Any]) -> None:
    """
    body must include:
    - to: E.164 without +
    - kind: 'template' | 'session'
    For template: template_name, language_code
    For session: session_active must be True (client attests user messaged within 24h window)
    """
    to = body.get("to")
    if not to or not str(to).isdigit():
        raise WhatsAppPolicyError("to must be E.164 digits without + prefix")
    kind = body.get("kind")
    if kind not in ("template", "session"):
        raise WhatsAppPolicyError("kind must be 'template' or 'session'")
    if kind == "template":
        if not body.get("template_name"):
            raise WhatsAppPolicyError("template_name required for template sends")
        if not body.get("language_code"):
            raise WhatsAppPolicyError("language_code required for template sends")
    if kind == "session" and not body.get("session_active"):
        raise WhatsAppPolicyError("session sends require session_active=true (24h window attestation)")


async def opt_in_allowed(redis, *, wa_id: str) -> bool:
    """Optional Redis-backed opt-in: SET whatsapp:optin:{wa_id} must exist."""
    if redis is None:
        return True
    v = await redis.get(f"whatsapp:optin:{wa_id}")
    return v == "1"


async def send_whatsapp_message(settings: Settings, redis, body: dict[str, Any]) -> dict[str, Any]:
    if not settings.whatsapp_access_token or not settings.whatsapp_phone_number_id:
        raise RuntimeError("WhatsApp not configured")

    validate_outbound_request(body)
    to = str(body["to"])
    if not await opt_in_allowed(redis, wa_id=to):
        raise WhatsAppPolicyError("Recipient has not opted in (whatsapp:optin not set)")

    url = (
        f"https://graph.facebook.com/{settings.whatsapp_api_version}/"
        f"{settings.whatsapp_phone_number_id}/messages"
    )
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}",
        "Content-Type": "application/json",
    }

    if body["kind"] == "template":
        graph_body: dict[str, Any] = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": body["template_name"],
                "language": {"code": body["language_code"]},
            },
        }
        comps = body.get("template_components")
        if comps:
            graph_body["template"]["components"] = comps
    else:
        text = body.get("text")
        if not text:
            raise WhatsAppPolicyError("session messages require text")
        graph_body = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"preview_url": bool(body.get("preview_url")), "body": text},
        }

    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(url, json=graph_body, headers=headers)
        if r.status_code >= 400:
            raise RuntimeError(f"WhatsApp API {r.status_code}: {r.text}")
        return r.json()
