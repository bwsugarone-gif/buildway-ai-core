# -*- coding: utf-8 -*-
"""Local human approval queue for CRM draft replies."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

QUEUE_DIR = Path(__file__).parent.parent.parent / "data" / "approval_queue"


def review_reasons(
    customer_message: str,
    confidence: str,
    kb_used: bool,
    conflict_warning: str | None = None,
) -> list[str]:
    text = str(customer_message or "").lower()
    reasons: list[str] = []
    if str(confidence or "").upper() == "LOW":
        reasons.append("Confidence LOW")
    if conflict_warning:
        reasons.append("conflict detected")
    if not kb_used:
        reasons.append("out-of-KB")
    if any(keyword in text for keyword in ["price", "pricing", "cost", "報價", "價錢", "價格"]):
        if not kb_used or str(confidence or "").upper() == "LOW":
            reasons.append("price missing")
    if any(keyword in text for keyword in ["shipping", "delivery", "freight", "運費", "送貨", "交期"]):
        if not kb_used or str(confidence or "").upper() == "LOW":
            reasons.append("shipping missing")
    return list(dict.fromkeys(reasons))


def needs_human_review(
    customer_message: str,
    confidence: str,
    kb_used: bool,
    conflict_warning: str | None = None,
) -> tuple[bool, list[str]]:
    reasons = review_reasons(customer_message, confidence, kb_used, conflict_warning)
    return bool(reasons), reasons


def enqueue_approval_item(
    tenant_id: str,
    customer_ref: str,
    customer_message: str,
    draft_reply: str,
    confidence: str,
    reason: str | list[str],
    provider: str = "",
    queue_dir: Path | None = None,
) -> dict[str, Any]:
    root = queue_dir or QUEUE_DIR
    root.mkdir(parents=True, exist_ok=True)
    reasons = reason if isinstance(reason, list) else [str(reason)]
    item = {
        "approval_id": f"APR-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}",
        "tenant_id": str(tenant_id or "demo_tenant"),
        "customer_ref": str(customer_ref or "CUST-001"),
        "customer_message": str(customer_message or ""),
        "draft_reply": str(draft_reply or ""),
        "confidence": str(confidence or "N/A"),
        "reason": reasons,
        "status": "Needs Human Review",
        "provider": str(provider or ""),
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    path = root / f"{item['approval_id']}.json"
    path.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
    return item


def list_approval_queue(queue_dir: Path | None = None) -> list[dict[str, Any]]:
    root = queue_dir or QUEUE_DIR
    if not root.exists():
        return []
    items: list[dict[str, Any]] = []
    for path in root.glob("APR-*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict):
            items.append(data)
    return sorted(items, key=lambda item: item.get("created_at", ""), reverse=True)
