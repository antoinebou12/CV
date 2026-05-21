"""Shared repository paths for scripts under scripts/."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_ROOT = REPO_ROOT / "scripts"


def script_path(*parts: str) -> Path:
    return SCRIPTS_ROOT.joinpath(*parts)
