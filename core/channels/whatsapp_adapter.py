# -*- coding: utf-8 -*-
"""WhatsApp webhook adapter placeholder.

This module is intentionally API-provider neutral. It does not call YCloud,
Twilio, 360dialog, or Meta Cloud API yet.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def parse_incoming_message(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize an incoming webhook-like payload into the CRM message shape."""
    payload = payload or {}
    message = payload.get("message") or payload.get("text") or {}
    if isinstance(message, dict):
        text = message.get("text") or message.get("body") or ""
    else:
        text = str(message or "")

    sender = (
        payload.get("from")
        or payload.get("sender")
        or payload.get("wa_id")
        or payload.get("phone")
        or ""
    )
    return {
        "channel": "whatsapp",
        "provider": payload.get("provider", "placeholder"),
        "message_id": payload.get("message_id") or payload.get("id") or "",
        "customer_ref": str(sender or "unknown"),
        "customer_message": str(text or ""),
        "received_at": payload.get("timestamp")
        or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "raw_payload": payload,
    }


def build_reply_payload(message: dict[str, Any]) -> dict[str, Any]:
    """Build a provider-neutral reply payload for future WhatsApp connectors."""
    message = message or {}
    return {
        "channel": "whatsapp",
        "to": message.get("customer_ref") or message.get("to") or "",
        "type": "text",
        "text": {
            "body": message.get("reply") or message.get("draft_reply") or "",
        },
        "metadata": {
            "tenant_id": message.get("tenant_id", "demo_tenant"),
            "source": "buildway-ai-core-placeholder",
        },
    }


def send_reply(payload: dict[str, Any]) -> dict[str, Any]:
    """Placeholder send function. No external WhatsApp API is called."""
    return {
        "sent": False,
        "status": "placeholder_only",
        "message": "WhatsApp API is not connected in Phase 0.9 placeholder.",
        "payload": payload,
    }
