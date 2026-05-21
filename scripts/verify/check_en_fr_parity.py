"""Ensure EN/FR static CV HTML stay structurally aligned."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import sys

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT as ROOT
EN = ROOT / "index-en.html"
FR = ROOT / "index-fr.html"

COUNTS = [
    ("cv-section", r'<details class="box cv-section"'),
    ("cv-job", r'<details class="cv-job'),
    ("skill-group", r'class="skill-group"'),
    ("project-card", r'class="project-card'),
    ("credly-badge", r"credly\.com/badges/[a-f0-9-]+"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def credly_uuids(html: str) -> set[str]:
    return set(re.findall(r"credly\.com/badges/([a-f0-9-]+)", html))


def main() -> int:
    if not EN.is_file() or not FR.is_file():
        print("Missing index-en.html or index-fr.html")
        return 1

    en, fr = read(EN), read(FR)
    errs: list[str] = []

    for label, pattern in COUNTS:
        en_n = len(re.findall(pattern, en))
        fr_n = len(re.findall(pattern, fr))
        if en_n != fr_n:
            errs.append(f"{label}: EN={en_n} FR={fr_n}")

    en_cred = credly_uuids(en)
    fr_cred = credly_uuids(fr)
    if en_cred != fr_cred:
        only_en = en_cred - fr_cred
        only_fr = fr_cred - en_cred
        if only_en:
            errs.append(f"credly only in EN: {sorted(only_en)}")
        if only_fr:
            errs.append(f"credly only in FR: {sorted(only_fr)}")

    if errs:
        print("EN/FR parity check FAILED:")
        for e in errs:
            print(f"  {e}")
        return 1
    print("EN/FR parity check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
