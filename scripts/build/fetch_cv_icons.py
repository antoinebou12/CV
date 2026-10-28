"""Store the CV's technology logos locally and point the pages at the copies.

python scripts/build/fetch_cv_icons.py [--check]

Finds Simple Icons and devicon CDN images in index.html, index-en.html and
index-fr.html, downloads each SVG once into images/tech-icons/, removes anything
executable, and rewrites the src to the local file. Local files load from the
same origin as the page, so the expertise widget no longer waits on two CDNs.
--check only reports remote icons and missing local files (exit 1 if any).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
PAGES = [ROOT / name for name in ("index.html", "index-en.html", "index-fr.html")]
FOLDER = ROOT / "images/tech-icons"
REMOTE = re.compile(
    r"https://cdn\.simpleicons\.org/(?P<slug>[\w.-]+)"
    r"|https://cdn\.jsdelivr\.net/gh/devicons/devicon@[\w.]+/icons/[\w-]+/(?P<file>[\w-]+)\.svg"
)
# Corrections applied before download: a logo that 404s or names the wrong product.
REPLACE = {
    # Simple Icons has no Karma logo; devicon does.
    "https://cdn.simpleicons.org/karma": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/karma/karma-original.svg",
}


def local_name(match):
    if match["slug"]:
        return f"{match['slug']}.svg"
    return re.sub(r"-original(?:-wordmark)?$|-plain$", "", match["file"]) + ".svg"


def sanitize(svg):
    svg = re.sub(r"<script\b.*?</script>", "", svg, flags=re.DOTALL | re.IGNORECASE)
    svg = re.sub(r"<foreignObject\b.*?</foreignObject>", "", svg, flags=re.DOTALL | re.IGNORECASE)
    svg = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", svg, flags=re.IGNORECASE)
    if "<svg" not in svg[:400]:
        raise ValueError("not an SVG")
    return svg.strip() + "\n"


def download(url):
    request = Request(url, headers={"User-Agent": "CV-icon-cache/1.0"})
    with urlopen(request, timeout=30) as response:
        body = response.read(200_001)
    if len(body) > 200_000:
        raise ValueError("icon larger than 200 KB")
    return sanitize(body.decode("utf-8"))


def fix_mcp_chip(text):
    """The MCP skill chip shows the protocol's own logo; Anthropic's stays on the Claude Academy badge."""
    return re.sub(
        r'(<li class="expertise-pill" data-skill="MCP">(?:(?!</li>).)*?class="expertise-pill-icon"[^>]*?src=")https://cdn\.simpleicons\.org/anthropic"',
        r'\1https://cdn.simpleicons.org/modelcontextprotocol"',
        text,
        flags=re.DOTALL,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report remote or missing icons without changing files")
    args = parser.parse_args()
    problems = []
    cache = {}
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        original = text
        if args.check:
            problems += [f"{page.name}: remote icon {m[0]}" for m in REMOTE.finditer(text)]
            for path in set(re.findall(r'src="(images/tech-icons/[\w.-]+\.svg)"', text)):
                if not (ROOT / path).exists():
                    problems.append(f"{page.name}: missing {path}")
            continue
        text = fix_mcp_chip(text)
        for remote, replacement in REPLACE.items():
            text = text.replace(f'src="{remote}"', f'src="{replacement}"')

        def localize(match):
            url = match[0]
            name = local_name(match)
            target = FOLDER / name
            if name not in cache:
                if not target.exists():
                    FOLDER.mkdir(parents=True, exist_ok=True)
                    target.write_text(download(url), encoding="utf-8")
                    print(f"saved {name} from {url}")
                cache[name] = f"images/tech-icons/{name}"
            return cache[name]

        text = REMOTE.sub(localize, text)
        if text != original:
            page.write_text(text, encoding="utf-8")
            print(f"updated {page.name}")
    if problems:
        print("\n".join(problems))
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
