"""Snapshot the CV's stats widgets as local SVG files.

python scripts/build/fetch_cv_widgets.py [--check]

The GitHub stats, top-languages and WakaTime cards and the LeetCode badges change
slowly, so the CV serves saved copies from images/widgets/ instead of waiting on
third-party renderers (the previous github-readme-stats-fast deployment was
disabled and every card failed). Spotify "now playing" stays live by design.
Rerun this script to refresh the numbers; --check fails if a card is missing.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.parse import unquote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
PAGES = [ROOT / name for name in ("index.html", "index-en.html", "index-fr.html")]
FOLDER = ROOT / "images/widgets"
STATS = "https://github-readme-stats.vercel.app/api"
CARDS = {
    # Old (disabled) and current renderer paths map to one local file each.
    "github-stats.svg": (r"https://github-readme-stats(?:-fast)?\.vercel\.app/api\?[^\"]*",
                          f"{STATS}?username=antoinebou12&theme=dark&show_icons=true&hide_border=true"),
    "github-top-languages.svg": (r"https://github-readme-stats(?:-fast)?\.vercel\.app/api/top-langs/?\?[^\"]*",
                                 f"{STATS}/top-langs/?username=antoinebou12&theme=dark&hide_border=true&layout=compact&langs_count=8"),
    "wakatime.svg": (r"https://github-readme-stats(?:-fast)?\.vercel\.app/api/wakatime\?[^\"]*",
                     f"{STATS}/wakatime?username=antoinebou13&theme=dark&hide_border=true"),
}
BADGE = re.compile(r"https://img\.shields\.io/badge/([\w%.-]+)")


def sanitize(svg):
    svg = re.sub(r"<script\b.*?</script>", "", svg, flags=re.DOTALL | re.IGNORECASE)
    svg = re.sub(r"<foreignObject\b.*?</foreignObject>", "", svg, flags=re.DOTALL | re.IGNORECASE)
    svg = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", svg, flags=re.IGNORECASE)
    if "<svg" not in svg[:600]:
        raise ValueError("renderer did not return SVG")
    if re.search(r"Something went wrong|DEPLOYMENT_DISABLED|rate limit", svg, re.IGNORECASE):
        raise ValueError("renderer returned an error card")
    return svg.strip() + "\n"


def download(url):
    request = Request(url, headers={"User-Agent": "CV-widget-snapshot/1.0"})
    with urlopen(request, timeout=45) as response:
        body = response.read(500_001)
    if len(body) > 500_000:
        raise ValueError("widget larger than 500 KB")
    return sanitize(body.decode("utf-8"))


def badge_name(path):
    return re.sub(r"[^a-z0-9]+", "-", unquote(path).lower()).strip("-") + ".svg"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if a widget is remote or missing")
    args = parser.parse_args()
    FOLDER.mkdir(parents=True, exist_ok=True)
    problems = []
    if not args.check:
        for name, (_, url) in CARDS.items():
            (FOLDER / name).write_text(download(url), encoding="utf-8")
            print(f"saved {name}")
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        original = text
        for name, (pattern, _) in CARDS.items():
            text = re.sub(f'(data-src|src)="{pattern}"', rf'\1="images/widgets/{name}"', text)
        for match in set(BADGE.findall(html.unescape(text))):
            name = badge_name(match)
            if not args.check and not (FOLDER / name).exists():
                (FOLDER / name).write_text(download(f"https://img.shields.io/badge/{match}"), encoding="utf-8")
                print(f"saved {name}")
            text = text.replace(f"https://img.shields.io/badge/{match}", f"images/widgets/{name}")
        if args.check:
            if text != original:
                problems.append(f"{page.name}: remote stats widget or badge")
            for path in set(re.findall(r'"(images/widgets/[\w.-]+\.svg)"', original)):
                if not (ROOT / path).exists():
                    problems.append(f"{page.name}: missing {path}")
        elif text != original:
            page.write_text(text, encoding="utf-8")
            print(f"updated {page.name}")
    if problems:
        print("\n".join(problems))
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
