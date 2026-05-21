"""Tests for AEO page generation."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _about_html(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_about_pages_have_faq_schema() -> None:
    for name in ("about-en.html", "about-fr.html"):
        html = _about_html(name)
        assert "FAQPage" in html, f"{name} missing FAQPage JSON-LD"
        assert "aeo-faq-answer" in html
        assert 'class="cv-faq-item"' in html
        assert re.search(r'id="faq-', html), f"{name} missing FAQ question ids"


def test_about_page_layout() -> None:
    for name in ("about-en.html", "about-fr.html"):
        html = _about_html(name)
        assert "cv-about-page.css" in html
        assert "photo-header" in html
        assert 'class="container cv-about-page"' in html
        assert html.count('class="box cv-section"') == 4
        assert html.count('class="cv-faq-item"') == 6
        assert html.count('class="list-group-item"') >= 9


def test_about_en_fr_structural_parity() -> None:
    en = _about_html("about-en.html")
    fr = _about_html("about-fr.html")
    for needle in (
        "cv-faq-item",
        "box cv-section",
        "photo-header",
        "btn btn-primary",
    ):
        assert en.count(needle) == fr.count(needle), f"parity mismatch: {needle}"


def test_cv_has_lead_and_freshness() -> None:
    for name in ("index-en.html", "index-fr.html"):
        html = (ROOT / name).read_text(encoding="utf-8")
        assert "aeo-lead" in html
        assert "aeo-agent-only" in html
        assert "article:modified_time" in html
        assert "cv-last-updated" in html
        assert "about-en.html" in html or "about-fr.html" in html


def test_regenerate_is_idempotent() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build" / "generate_aeo_content.py"), "--all"],
        cwd=ROOT,
        check=True,
    )
    for name in ("about-en.html", "about-fr.html"):
        graph = re.search(
            r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
            _about_html(name),
            re.DOTALL,
        )
        assert graph
        data = json.loads(graph.group(1))
        types = [n.get("@type") for n in data.get("@graph", [])]
        assert "FAQPage" in types
        person = next(n for n in data["@graph"] if n.get("@type") == "Person")
        assert "knowsAbout" in person


if __name__ == "__main__":
    test_about_pages_have_faq_schema()
    test_about_page_layout()
    test_about_en_fr_structural_parity()
    test_cv_has_lead_and_freshness()
    test_regenerate_is_idempotent()
    print("ok")
