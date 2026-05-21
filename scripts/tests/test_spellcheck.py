"""Tests for locale-scoped spellcheck path lists."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "ci"))

import spellcheck  # noqa: E402


def test_en_and_fr_paths_do_not_overlap() -> None:
    en = {p.resolve() for p in spellcheck.collect_paths("en")}
    fr = {p.resolve() for p in spellcheck.collect_paths("fr")}
    overlap = en & fr
    assert not overlap, f"paths in both locales: {sorted(overlap)[:5]}"


def test_key_cv_files_are_scoped() -> None:
    en = {p.name for p in spellcheck.collect_paths("en")}
    fr = {p.name for p in spellcheck.collect_paths("fr")}
    assert "index-en.html" in en
    assert "index-fr.html" in fr
    assert "index-fr.html" not in en
    assert "index-en.html" not in fr


def test_hugo_fr_markdown_suffix() -> None:
    fr = spellcheck.collect_paths("fr")
    fr_md = [p for p in fr if p.suffix == ".md"]
    assert fr_md, "expected French Hugo markdown files"
    assert all(
        p.name.endswith(".fr.md") or p.name == "search.fr.md" for p in fr_md
    )


def test_hugo_en_excludes_fr_markdown() -> None:
    en = spellcheck.collect_paths("en")
    en_md = [p for p in en if p.suffix == ".md" and "hugo" in p.as_posix()]
    assert en_md, "expected English Hugo markdown files"
    assert not any(p.name.endswith(".fr.md") for p in en_md)
