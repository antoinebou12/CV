# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow>=10"]
# ///
"""Serve right-sized images on the CV pages.

uv run scripts/build/optimize_cv_images.py [--check]

Gallery thumbnails are shown at 140-300 px but were full screenshots (800-1024 px PNG);
they get a 640 px WebP beside the original, and the full-size viewer keeps the original
through data-image-preview-src. Organisation logos are shown at 28 px and get a 112 px
copy when the source is larger. The portrait gets 208/416 px WebP candidates in srcset.
Generated files sit next to their source; rerunning skips work already done.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PAGES = [ROOT / name for name in ("index-en.html", "index-fr.html")]
GALLERY_WIDTH = 640
LOGO_WIDTH = 112
PORTRAIT = ("antoine-portrait.png", (208, 416))


def resized(source: Path, width: int, suffix: str, fmt: str, convert_only: bool = False) -> Path | None:
    """Write a copy at most `width` px wide; None when the source is already small enough.

    With convert_only, a source narrower than `width` is re-encoded at its own size instead.
    """
    target = source.with_name(f"{source.stem}-{width}{suffix}")
    if target.exists():
        return target
    with Image.open(source) as image:
        if image.width <= width * 1.1 and not convert_only:
            return None
        width = min(width, image.width)
        height = round(image.height * width / image.width)
        copy = image.convert("RGBA" if image.mode in ("RGBA", "LA", "P") else "RGB").resize((width, height), Image.LANCZOS)
        if fmt == "WEBP":
            copy.save(target, fmt, quality=82, method=6)
        else:
            copy.save(target, fmt, optimize=True)
    return target


def rewrite(html: str) -> tuple[str, list[str]]:
    changes = []

    def gallery(match: re.Match) -> str:
        tag = match[0]
        src = re.search(r'src="((?:papers|images)/[^"]+\.(?:png|jpe?g))"', tag)
        if not src or not (ROOT / src[1]).exists():
            return tag
        thumb = resized(ROOT / src[1], GALLERY_WIDTH, ".webp", "WEBP")
        if not thumb:
            return tag
        rel = thumb.relative_to(ROOT).as_posix()
        changes.append(f"{src[1]} -> {rel}")
        return tag.replace(f'src="{src[1]}"', f'src="{rel}"')

    # Thumbnails inside the full-size viewer buttons (the viewer itself reads data-image-preview-src).
    html = re.sub(r'(?s)(<button[^>]*data-image-preview-src="[^"]+"[^>]*>\s*)(<img[^>]*>)',
                  lambda m: m[1] + gallery(re.match(r'.*', m[2], re.S)), html)

    def logo(match: re.Match) -> str:
        tag, path = match[0], match[1]
        if not (ROOT / path).exists():
            return tag
        small = resized(ROOT / path, LOGO_WIDTH, Path(path).suffix, "PNG" if path.endswith(".png") else "JPEG")
        if not small:
            return tag
        rel = small.relative_to(ROOT).as_posix()
        changes.append(f"{path} -> {rel}")
        return tag.replace(f'src="{path}"', f'src="{rel}"')

    html = re.sub(r'<img[^>]*class="job-org-logo[^"]*"[^>]*src="(images/org-logos/[\w.-]+?(?<!-112)\.(?:png|jpe?g))"[^>]*>', logo, html)

    name, widths = PORTRAIT
    # The 2x candidate may be the source size itself; it still saves most of the PNG's weight as WebP.
    candidates = [resized(ROOT / name, w, ".webp", "WEBP", convert_only=True) for w in widths]
    if all(candidates):
        # Declare each file's real width: the largest candidate cannot exceed the source.
        srcset = ", ".join(f"{c.relative_to(ROOT).as_posix()} {Image.open(c).width}w" for c in candidates)
        new = f'srcset="{srcset}"'
        if f'srcset="{name} 400w"' in html:
            html = html.replace(f'srcset="{name} 400w"', new)
            changes.append(f"{name} srcset -> {srcset}")
    return html, changes


def write(page: Path, text: str) -> None:
    """Windows briefly locks the CV pages while other tools read them; retry before giving up."""
    for attempt in range(20):
        try:
            page.write_text(text, encoding="utf-8")
            return
        except OSError:
            time.sleep(0.5)
    raise SystemExit(f"{page.name} stayed locked; rerun the script")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if a page still references an oversized image")
    args = parser.parse_args()
    pending = 0
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        updated, changes = rewrite(text)
        pending += len(changes)
        for change in changes:
            print(f"{page.name}: {change}")
        if not args.check and updated != text:
            write(page, updated)
    if args.check and pending:
        return 1
    print("CV images are right-sized." if not pending or not args.check else "")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
