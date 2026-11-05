"""Fail when an indexable HTML page of the built site is missing from the root sitemap.

Redirect stubs (meta refresh), pages marked noindex and 404 pages are not indexable.
Usage: python scripts/verify/check_sitemap_coverage.py --site-dir <built site> [--site-root URL]
"""
import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote

REFRESH = re.compile(r"http-equiv=[\"']?refresh", re.I)
NOINDEX = re.compile(r"<meta[^>]+name=[\"']?robots[\"']?[^>]+noindex", re.I)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--site-dir", required=True)
    parser.add_argument("--site-root", default="https://antoineboucher.info/CV")
    args = parser.parse_args()
    site = Path(args.site_dir)
    listed = {unquote(loc) for loc in re.findall(r"<loc>([^<]+)</loc>", (site / "sitemap.xml").read_text(encoding="utf-8"))}
    missing = []
    for page in sorted(site.rglob("*.html")):
        relative = page.relative_to(site).as_posix()
        if page.name == "404.html":
            continue
        head = page.read_text(encoding="utf-8", errors="ignore")[:6000]
        if REFRESH.search(head) or NOINDEX.search(head):
            continue
        url = f"{args.site_root}/{relative}"
        if page.name == "index.html" and relative != "index.html":
            url = url[: -len("index.html")]
        if url not in listed:
            missing.append(url)
    for url in missing:
        print(f"Missing from sitemap.xml: {url}")
    print(f"Sitemap lists {len(listed)} URLs; {len(missing)} indexable pages missing.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
