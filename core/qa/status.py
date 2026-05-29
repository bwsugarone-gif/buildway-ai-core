# -*- coding: utf-8 -*-
"""Local QA status helpers for the Streamlit SaaS foundation demo."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent.parent.parent / "data"
QA_STATUS_FILE = DATA_DIR / "qa_status.json"

QA_CHECKLIST = [
    "Out-of-KB 問題",
    "垃圾輸入",
    "假資料誘導",
    "價格陷阱",
    "Shipping trap",
    "中文問題",
    "中英混合",
    "WhatsApp demo flow",
]


def default_qa_status() -> dict[str, Any]:
    return {
        "last_run": "",
        "passed_count": 0,
        "failed_count": 0,
        "notes": "尚未執行 QA。請依 docs/PHASE_0_6_QA_RESULTS.md checklist 手動或自動記錄。",
        "checklist": QA_CHECKLIST,
    }


def load_qa_status(path: Path | None = None) -> dict[str, Any]:
    status_path = path or QA_STATUS_FILE
    if not status_path.exists():
        return default_qa_status()
    try:
        data = json.loads(status_path.read_text(encoding="utf-8"))
    except Exception:
        return default_qa_status()
    status = default_qa_status()
    if isinstance(data, dict):
        status.update(data)
    return status


def save_qa_status(
    passed_count: int,
    failed_count: int,
    notes: str = "",
    path: Path | None = None,
) -> dict[str, Any]:
    status_path = path or QA_STATUS_FILE
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status = {
        "last_run": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "passed_count": int(passed_count),
        "failed_count": int(failed_count),
        "notes": notes,
        "checklist": QA_CHECKLIST,
    }
    status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    return status
