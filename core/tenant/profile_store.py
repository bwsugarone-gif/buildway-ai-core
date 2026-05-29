# -*- coding: utf-8 -*-
"""Local tenant profile storage for Phase 0.7 foundation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "tenants"
DEFAULT_TENANT_ID = "demo_tenant"
DEFAULT_TENANT_FILE = DATA_DIR / f"{DEFAULT_TENANT_ID}.json"

DEFAULT_TENANT_PROFILE: dict[str, Any] = {
    "tenant_id": DEFAULT_TENANT_ID,
    "company_name": "Demo Trading Company",
    "industry": "Foreign Trade",
    "default_language": "繁體中文",
    "reply_tone": "專業友善",
    "ai_provider": "OpenAI",
    "kb_collection_name": "demo_tenant_kb",
    "human_review_threshold": 0.65,
    "auto_reply_allowed": False,
}


def load_profile(path: Path | None = None) -> dict[str, Any]:
    profile_path = path or DEFAULT_TENANT_FILE
    if not profile_path.exists():
        return dict(DEFAULT_TENANT_PROFILE)
    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
    except Exception:
        return dict(DEFAULT_TENANT_PROFILE)
    profile = dict(DEFAULT_TENANT_PROFILE)
    if isinstance(data, dict):
        profile.update(data)
    return profile


def save_profile(profile: dict[str, Any], path: Path | None = None) -> dict[str, Any]:
    profile_path = path or DEFAULT_TENANT_FILE
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    current = load_profile(profile_path)
    current.update(profile or {})
    current["tenant_id"] = str(current.get("tenant_id") or DEFAULT_TENANT_ID)
    profile_path.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")
    return current
