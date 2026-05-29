# -*- coding: utf-8 -*-
"""Persistent customer interaction memory for CRM replies."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "customer_memory"
MAX_HISTORY_PER_CUSTOMER = 100


def _safe_name(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in str(value or ""))
    return cleaned.strip("_") or "unknown"


def _history_path(tenant_id: str, customer_ref: str, base_dir: Path | None = None) -> Path:
    root = base_dir or DATA_DIR
    return root / _safe_name(tenant_id) / f"{_safe_name(customer_ref)}.json"


def _load_history(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    return data if isinstance(data, list) else []


def save_customer_interaction(
    tenant_id: str,
    customer_ref: str,
    customer_message: str,
    ai_reply: str,
    confidence: str,
    kb_used: bool,
    provider: str,
    base_dir: Path | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Append one CRM interaction to persistent customer memory."""
    path = _history_path(tenant_id, customer_ref, base_dir=base_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "interaction_id": f"INT-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}",
        "tenant_id": str(tenant_id or "demo_tenant"),
        "customer_ref": str(customer_ref or "CUST-001"),
        "customer_message": str(customer_message or ""),
        "ai_reply": str(ai_reply or ""),
        "confidence": str(confidence or "N/A"),
        "kb_used": bool(kb_used),
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "provider": str(provider or ""),
    }
    if extra:
        record.update(extra)

    history = _load_history(path)
    history.append(record)
    history = history[-MAX_HISTORY_PER_CUSTOMER:]
    path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def list_customer_history(
    tenant_id: str,
    customer_ref: str,
    base_dir: Path | None = None,
) -> list[dict[str, Any]]:
    """Return newest-first customer interaction history."""
    history = _load_history(_history_path(tenant_id, customer_ref, base_dir=base_dir))
    return sorted(history, key=lambda item: item.get("timestamp", ""), reverse=True)
