#!/usr/bin/env python3
"""Append static site-root pages to sitemap.xml after copying Hugo's blog sitemap to _site root."""
from __future__ import annotations

import argparse
import sys
from xml.etree import ElementTree as ET

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def q(tag: str) -> str:
    return f"{{{NS}}}{tag}"


def existing_locs(urlset: ET.Element) -> set[str]:
    out: set[str] = set()
    for url_el in urlset.findall(q("url")):
        loc_el = url_el.find(q("loc"))
        if loc_el is not None and loc_el.text:
            out.add(loc_el.text.strip())
    return out


def add_url(urlset: ET.Element, loc: str, lastmod: str, existing: set[str]) -> None:
    if loc in existing:
        return
    u = ET.SubElement(urlset, q("url"))
    loc_el = ET.SubElement(u, q("loc"))
    loc_el.text = loc
    lm = ET.SubElement(u, q("lastmod"))
    lm.text = lastmod
    existing.add(loc)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, help="Path to existing sitemap (Hugo blog copy)")
    p.add_argument("--output", required=True, help="Path to write merged sitemap")
    p.add_argument(
        "--site-root",
        required=True,
        help="Public site root URL without trailing slash, e.g. https://antoineboucher.info/CV",
    )
    p.add_argument("--lastmod", required=True, help="YYYY-MM-DD for appended static URLs")
    args = p.parse_args()

    site_root = args.site_root.rstrip("/")
    tree = ET.parse(args.input)
    urlset = tree.getroot()
    if urlset.tag != q("urlset"):
        print(f"ERROR: expected urlset root, got {urlset.tag!r}", file=sys.stderr)
        return 1

    existing = existing_locs(urlset)
    static_paths = (
        "index-en.html",
        "index-fr.html",
        "index.html",
        "linktree/",
    )
    for path in static_paths:
        loc = f"{site_root}/{path}"
        add_url(urlset, loc, args.lastmod, existing)

    ET.register_namespace("", NS)
    ET.indent(tree, space="  ")
    tree.write(args.output, encoding="utf-8", xml_declaration=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
