# -*- coding: utf-8 -*-
"""Persistent tenant profile memory."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.tenant.profile_store import load_profile, save_profile


def save_tenant_profile(profile: dict[str, Any], path: Path | None = None) -> dict[str, Any]:
    """Save tenant profile to local JSON storage."""
    return save_profile(profile, path=path)


def load_tenant_profile(path: Path | None = None) -> dict[str, Any]:
    """Load tenant profile from local JSON storage."""
    return load_profile(path=path)
