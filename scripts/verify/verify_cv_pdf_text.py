#!/usr/bin/env python3
"""Smoke-check CV PDF text extraction (ATS-friendly pdftotext output)."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT

EN_FORBIDDEN = (
    "ENGiNEER",
    "GRAPHiCS",
    "ob-servability",
    "ob‑servability",  # U+2011 non-breaking hyphen
)
EN_REGEX = (
    (re.compile(r"MAY\s+20,\s+20\d{2}", re.I), "footer compile date leaked into body"),
    (re.compile(r"1IONODES"), "page number glued to employer name"),
)

FR_FORBIDDEN = (
    "ob-servabilité",
    "ob‑servabilité",
)
FR_REGEX = (
    (re.compile(r"1IONODES", re.I), "page number glued to employer name"),
)


def pdftotext(pdf: Path) -> str:
    exe = shutil.which("pdftotext")
    if not exe:
        raise RuntimeError("pdftotext not found on PATH (install Poppler)")
    proc = subprocess.run(
        [exe, str(pdf), "-"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"pdftotext failed for {pdf}: {proc.stderr}")
    return proc.stdout


def check_pdf(pdf: Path, lang: str) -> list[str]:
    if not pdf.is_file():
        return [f"missing PDF: {pdf}"]

    text = pdftotext(pdf)
    issues: list[str] = []

    if lang == "en":
        forbidden = EN_FORBIDDEN
        patterns = EN_REGEX
    else:
        forbidden = FR_FORBIDDEN
        patterns = FR_REGEX

    for needle in forbidden:
        if needle in text:
            issues.append(f"forbidden substring: {needle!r}")

    for pattern, msg in patterns:
        if pattern.search(text):
            issues.append(msg)

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lang",
        choices=("en", "fr", "all"),
        default="all",
        help="Which CV PDF(s) to check",
    )
    args = parser.parse_args()

    targets: list[tuple[str, Path]] = []
    if args.lang in ("en", "all"):
        targets.append(("en", REPO_ROOT / "cv-en" / "resume.pdf"))
    if args.lang in ("fr", "all"):
        targets.append(("fr", REPO_ROOT / "cv-fr" / "resume.pdf"))

    failed = False
    for lang, pdf in targets:
        issues = check_pdf(pdf, lang)
        if issues:
            failed = True
            print(f"FAIL {pdf}:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"OK {pdf}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
