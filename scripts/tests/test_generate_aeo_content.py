"""Tests for AEO CV patches (lead, freshness, nav)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_cv_has_lead_and_freshness() -> None:
    for name in ("index-en.html", "index-fr.html"):
        html = (ROOT / name).read_text(encoding="utf-8")
        assert "aeo-lead" in html
        assert "aeo-agent-only" in html
        assert "article:modified_time" in html
        assert "cv-last-updated" in html
        assert "about-en.html" not in html
        assert "about-fr.html" not in html


def test_about_pages_removed() -> None:
    for name in ("about-en.html", "about-fr.html"):
        assert not (ROOT / name).exists(), f"{name} should be removed"


def test_regenerate_is_idempotent() -> None:
    script = str(ROOT / "scripts" / "build" / "generate_aeo_content.py")
    cmd = [sys.executable, script, "--all"]
    subprocess.run(cmd, cwd=ROOT, check=True)
    cv_targets = ("index-en.html", "index-fr.html", "index.html")
    after_first = {name: (ROOT / name).read_bytes() for name in cv_targets}
    subprocess.run(cmd, cwd=ROOT, check=True)
    after_second = {name: (ROOT / name).read_bytes() for name in cv_targets}
    assert after_first == after_second, "second --all run must not change committed CV HTML"
    assert not (ROOT / "about-en.html").exists()
    assert not (ROOT / "about-fr.html").exists()


if __name__ == "__main__":
    test_cv_has_lead_and_freshness()
    test_about_pages_removed()
    test_regenerate_is_idempotent()
    print("ok")
