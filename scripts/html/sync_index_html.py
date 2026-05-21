#!/usr/bin/env python3
"""Sync root index.html from index-en.html (modern CV layout and styles)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT
SITE_ROOT = "https://antoineboucher.info/CV"
SRC = REPO_ROOT / "index-en.html"
DST = REPO_ROOT / "index.html"
PAGE_OLD = f"{SITE_ROOT}/index-en.html"
PAGE_NEW = f"{SITE_ROOT}/index.html"


def sync_index_html() -> None:
    if not SRC.is_file():
        raise FileNotFoundError(f"Missing source: {SRC}")
    html = SRC.read_text(encoding="utf-8")
    html = html.replace(PAGE_OLD, PAGE_NEW)
    html = html.replace(
        'href="index-en.html" class="current"',
        'href="index.html" class="current"',
    )
    DST.write_text(html, encoding="utf-8", newline="\n")
    print(f"Synced {DST} from {SRC.name}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if index.html differs from what sync would write",
    )
    args = p.parse_args()
    try:
        if args.check:
            expected = SRC.read_text(encoding="utf-8")
            expected = expected.replace(PAGE_OLD, PAGE_NEW).replace(
                'href="index-en.html" class="current"',
                'href="index.html" class="current"',
            )
            actual = DST.read_text(encoding="utf-8") if DST.is_file() else ""
            if actual != expected:
                print(
                    "index.html is out of date; run: python scripts/html/sync_index_html.py",
                    file=sys.stderr,
                )
                return 1
            print("index.html is in sync with index-en.html")
            return 0
        sync_index_html()
        return 0
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
