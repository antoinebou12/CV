"""Losslessly recompress PNG assets under papers/ and root hero image."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import sys

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT as ROOT
TARGETS = [ROOT / "antoine.png", ROOT / "papers"]


def optimize(path: Path) -> tuple[int, int]:
    try:
        from PIL import Image
    except ImportError:
        raise RuntimeError("Pillow required: pip install Pillow") from None

    before = path.stat().st_size
    img = Image.open(path)
    img.save(path, optimize=True)
    after = path.stat().st_size
    return before, after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="List PNGs only")
    args = parser.parse_args()

    pngs: list[Path] = []
    for base in TARGETS:
        if base.is_file() and base.suffix.lower() == ".png":
            pngs.append(base)
        elif base.is_dir():
            pngs.extend(sorted(base.rglob("*.png")))

    if not pngs:
        print("No PNG files found.")
        return 0

    if args.dry_run:
        for p in pngs:
            print(p.relative_to(ROOT))
        return 0

    total_before = total_after = 0
    for p in pngs:
        before, after = optimize(p)
        total_before += before
        total_after += after
        print(f"{p.relative_to(ROOT)}: {before} -> {after} bytes")
    saved = total_before - total_after
    print(f"Total saved: {saved} bytes ({len(pngs)} files)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as exc:
        print(exc)
        sys.exit(1)
