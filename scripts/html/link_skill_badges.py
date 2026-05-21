"""Link competence skill badges to official docs (index-en.html, index-fr.html)."""
from __future__ import annotations

import re
from pathlib import Path

import sys

_SCRIPTS = Path(__file__).resolve().parents[1]
_BUILD = _SCRIPTS / "build"
if str(_BUILD) not in sys.path:
    sys.path.insert(0, str(_BUILD))
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT as ROOT
from skill_urls import SKILL_URLS

SPAN_RE = re.compile(
    r'<span class="skill badge(?!\s+skill-badge-note)">([^<]+)</span>'
)

MARKERS = (
    ("<!-- COMPETENCES -->", "<!-- COMPÉTENCES -->"),
    ("<!-- COMPETENCES -->", "<!-- COMPÉTENCES -->"),
    ("<!-- RECOMMENDATIONS -->", "<!-- RECOMMANDATIONS -->"),
)


def link_badges(html: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        label = match.group(1)
        url = SKILL_URLS.get(label)
        if not url:
            return match.group(0)
        count += 1
        return (
            f'<a class="skill badge" href="{url}" target="_blank" '
            f'rel="noopener noreferrer">{label}</a>'
        )

    return SPAN_RE.sub(repl, html), count


def main() -> None:
    for name in ("index-en.html", "index-fr.html"):
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        new_text, n = link_badges(text)
        path.write_text(new_text, encoding="utf-8")
        print(f"{name}: linked {n} skill badges")


if __name__ == "__main__":
    main()
