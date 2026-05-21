"""Extract inline <style> blocks from index-en.html into css/cv-main.css and css/cv-print.css."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import sys

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT as ROOT
SRC = ROOT / "index-en.html"
CSS_DIR = ROOT / "css"
MAIN_CSS = CSS_DIR / "cv-main.css"
PRINT_CSS = CSS_DIR / "cv-print.css"
HTML_FILES = [ROOT / "index-en.html", ROOT / "index-fr.html"]

STYLE_BLOCK_RE = re.compile(
    r'  <style type="text/css">(.*?)</style>',
    re.DOTALL,
)
PRINT_STYLE_RE = re.compile(
    r'  <style type="text/css" media="print">(.*?)</style>',
    re.DOTALL,
)

LINKS = (
    '  <link rel="stylesheet" href="css/cv-main.css">\n'
    '  <link rel="stylesheet" href="css/cv-print.css" media="print">\n'
)


def extract_from_en() -> tuple[str, str]:
    html = SRC.read_text(encoding="utf-8")
    blocks = STYLE_BLOCK_RE.findall(html)
    if len(blocks) < 1:
        raise RuntimeError("Could not find main style block in index-en.html")
    main = blocks[0].strip("\n")
    print_match = PRINT_STYLE_RE.search(html)
    print_css = print_match.group(1).strip("\n") if print_match else ""
    return main, print_css


def patch_html(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    if "css/cv-main.css" in html:
        print(f"{path.name}: already links external CSS")
        return
    html = STYLE_BLOCK_RE.sub("", html, count=1)
    html = PRINT_STYLE_RE.sub("", html, count=1)
    insert_at = html.find('  <link rel="stylesheet" href="css/cv-site-nav.css">')
    if insert_at == -1:
        raise RuntimeError(f"cv-site-nav.css link not found in {path.name}")
    end = html.find("\n", insert_at) + 1
    html = html[:end] + LINKS + html[end:]
    path.write_text(html, encoding="utf-8", newline="\n")
    print(f"{path.name}: linked external CSS, removed inline styles")


def main() -> int:
    if not SRC.is_file():
        print(f"Missing {SRC}")
        return 1
    main_css, print_css = extract_from_en()
    CSS_DIR.mkdir(exist_ok=True)
    MAIN_CSS.write_text(main_css + "\n", encoding="utf-8", newline="\n")
    PRINT_CSS.write_text(print_css + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {MAIN_CSS.relative_to(ROOT)} ({len(main_css)} chars)")
    print(f"Wrote {PRINT_CSS.relative_to(ROOT)} ({len(print_css)} chars)")
    for path in HTML_FILES:
        patch_html(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
