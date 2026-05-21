"""Regenerate .aspell.fr.pws from current FR spellcheck paths.

Requires aspell and aspell-fr on PATH. Run after adding FR content:

    python scripts/ci/update_aspell_fr_pws.py
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT

from spellcheck import (  # noqa: E402
    ASPELL_FR_PWS,
    _aspell_unknown_words,
    collect_paths,
)

_COURSE_CODE_RE = re.compile(r"^[A-Z]{2,6}\d{2,5}$")
_DIGIT_RE = re.compile(r"\d")


def _unknown_words(path: Path, aspell: str, personal: list[str]) -> set[str]:
    text = path.read_text(encoding="utf-8")
    words = _aspell_unknown_words(path, text, aspell, personal)
    if words is None:
        raise RuntimeError(f"{path}: aspell failed")
    return {
        w
        for w in words
        if not _COURSE_CODE_RE.match(w) and not _DIGIT_RE.search(w)
    }


def main() -> int:
    aspell = shutil.which("aspell")
    if not aspell:
        print("aspell not found on PATH", file=sys.stderr)
        return 1

    existing: set[str] = set()
    if ASPELL_FR_PWS.is_file():
        for line in ASPELL_FR_PWS.read_text(encoding="utf-8").splitlines():
            word = line.strip()
            if word and not word.startswith("personal_ws"):
                existing.add(word)

    personal = ["-p", str(ASPELL_FR_PWS)] if ASPELL_FR_PWS.is_file() else []
    unknown: set[str] = set()
    for path in collect_paths("fr"):
        unknown |= _unknown_words(path, aspell, personal)

    merged = sorted(existing | unknown, key=lambda w: (w.lower(), w))
    lines = ["personal_ws-1.1 fr 0 utf-8", *merged]
    ASPELL_FR_PWS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    added = len(merged) - len(existing)
    print(f"Wrote {len(merged)} words to {ASPELL_FR_PWS.name} (+{added} new)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
