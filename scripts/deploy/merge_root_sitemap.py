#!/usr/bin/env python3
"""Append static site-root pages to sitemap.xml after copying Hugo's blog sitemap to _site root.

Hugo 0.160+ multilingual sites emit blog/sitemap.xml as a sitemapindex pointing at en/sitemap.xml
and fr/sitemap.xml. This script flattens that index into a single urlset at the site root.
"""
from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML_NS = "http://www.w3.org/1999/xhtml"

# (english path, french path) — x-default is always the English path
HREFLANG_PAIRS: tuple[tuple[str, str], ...] = (
    ("index-en.html", "index-fr.html"),
    ("about-en.html", "about-fr.html"),
    ("resume.md", "resume-fr.md"),
    ("resume.json", "resume-fr.json"),
)


def q(tag: str) -> str:
    return f"{{{NS}}}{tag}"


def xq(tag: str) -> str:
    return f"{{{XHTML_NS}}}{tag}"


def existing_locs(urlset: ET.Element) -> set[str]:
    out: set[str] = set()
    for url_el in urlset.findall(q("url")):
        loc_el = url_el.find(q("loc"))
        if loc_el is not None and loc_el.text:
            out.add(loc_el.text.strip())
    return out


def add_hreflang_alternates(url_el: ET.Element, en_path: str, fr_path: str, site_root: str) -> None:
    en_href = f"{site_root}/{en_path}"
    fr_href = f"{site_root}/{fr_path}"
    for hreflang, href in (
        ("en", en_href),
        ("fr", fr_href),
        ("x-default", en_href),
    ):
        link = ET.SubElement(url_el, xq("link"))
        link.set("rel", "alternate")
        link.set("hreflang", hreflang)
        link.set("href", href)


def add_url(
    urlset: ET.Element,
    loc: str,
    lastmod: str,
    existing: set[str],
    *,
    en_path: str | None = None,
    fr_path: str | None = None,
    site_root: str = "",
) -> None:
    if loc in existing:
        return
    u = ET.SubElement(urlset, q("url"))
    loc_el = ET.SubElement(u, q("loc"))
    loc_el.text = loc
    lm = ET.SubElement(u, q("lastmod"))
    lm.text = lastmod
    if en_path and fr_path and site_root:
        add_hreflang_alternates(u, en_path, fr_path, site_root)
    existing.add(loc)


def resolve_child_sitemap(blog_dir: Path, loc: str) -> Path:
    """Map a child sitemap URL from Hugo's index to a file under _site/blog/."""
    path = urlparse(loc).path
    marker = "/blog/"
    idx = path.find(marker)
    if idx == -1:
        raise ValueError(f"sitemap loc does not contain {marker!r}: {loc}")
    rel = path[idx + len(marker) :].lstrip("/")
    if not rel:
        raise ValueError(f"empty path after {marker!r} in {loc}")
    candidate = blog_dir / rel
    if not candidate.is_file():
        raise FileNotFoundError(f"child sitemap not found: {candidate} (from {loc})")
    return candidate


def merge_urlset_into(target: ET.Element, source: ET.Element, existing: set[str]) -> None:
    for url_el in source.findall(q("url")):
        loc_el = url_el.find(q("loc"))
        if loc_el is None or not loc_el.text:
            continue
        loc = loc_el.text.strip()
        if loc in existing:
            continue
        target.append(copy.deepcopy(url_el))
        existing.add(loc)


def load_urlset(input_path: Path, blog_dir: Path) -> ET.Element:
    tree = ET.parse(input_path)
    root = tree.getroot()
    if root.tag == q("urlset"):
        return root

    if root.tag != q("sitemapindex"):
        raise ValueError(f"expected urlset or sitemapindex root, got {root.tag!r}")

    merged: ET.Element | None = None
    existing: set[str] = set()
    for sm in root.findall(q("sitemap")):
        loc_el = sm.find(q("loc"))
        if loc_el is None or not loc_el.text:
            continue
        child_path = resolve_child_sitemap(blog_dir, loc_el.text.strip())
        child_root = ET.parse(child_path).getroot()
        if child_root.tag != q("urlset"):
            raise ValueError(
                f"expected urlset in {child_path}, got {child_root.tag!r}"
            )
        if merged is None:
            merged = ET.Element(q("urlset"))
            for key, value in child_root.attrib.items():
                merged.set(key, value)
        merge_urlset_into(merged, child_root, existing)

    if merged is None:
        merged = ET.Element(q("urlset"))
        merged.set("xmlns", NS)
    return merged


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, help="Path to existing sitemap (Hugo blog copy)")
    p.add_argument("--output", required=True, help="Path to write merged sitemap")
    p.add_argument(
        "--blog-dir",
        help="Directory containing Hugo blog output (default: <input-parent>/blog)",
    )
    p.add_argument(
        "--site-root",
        required=True,
        help="Public site root URL without trailing slash, e.g. https://antoineboucher.info/CV",
    )
    p.add_argument("--lastmod", required=True, help="YYYY-MM-DD for appended static URLs")
    args = p.parse_args()

    input_path = Path(args.input)
    blog_dir = Path(args.blog_dir) if args.blog_dir else input_path.parent / "blog"
    if not blog_dir.is_dir():
        print(f"ERROR: blog output directory not found: {blog_dir}", file=sys.stderr)
        return 1

    site_root = args.site_root.rstrip("/")
    try:
        urlset = load_urlset(input_path, blog_dir)
    except (ValueError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    existing = existing_locs(urlset)

    static_paths = (
        "index-en.html",
        "index-fr.html",
        "index.html",
        "about-en.html",
        "about-fr.html",
        "linktree/",
        "resume.md",
        "resume-fr.md",
        "resume.json",
        "resume-fr.json",
        "llms.txt",
    )
    for path in static_paths:
        loc = f"{site_root}/{path}"
        pair = next(
            ((en, fr) for en, fr in HREFLANG_PAIRS if path in (en, fr)),
            None,
        )
        if pair:
            en_path, fr_path = pair
            add_url(
                urlset,
                loc,
                args.lastmod,
                existing,
                en_path=en_path,
                fr_path=fr_path,
                site_root=site_root,
            )
        else:
            add_url(urlset, loc, args.lastmod, existing)

    out_tree = ET.ElementTree(urlset)
    ET.register_namespace("", NS)
    if "xmlns:xhtml" not in urlset.attrib:
        ET.register_namespace("xhtml", XHTML_NS)
    ET.indent(out_tree, space="  ")
    out_tree.write(args.output, encoding="utf-8", xml_declaration=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
