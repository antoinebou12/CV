#!/usr/bin/env python3
"""Validate a GitHub Pages deploy tree (_site) before upload.

Mirrors checks in .github/workflows/deploy.yml after Hugo build, promote, and sitemap merge.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def q(tag: str) -> str:
    return f"{{{NS}}}{tag}"


def validate_blog_nav(site_dir: Path, repo: str) -> None:
    index = site_dir / "blog" / "index.html"
    if not index.is_file():
        raise SystemExit(f"Missing {index}")
    text = index.read_text(encoding="utf-8", errors="replace")
    if f"/{repo}/blog/posts/" not in text:
        raise SystemExit(f"Expected /{repo}/blog/posts/ in blog index")
    if f"/{repo}/blog/search/" not in text:
        raise SystemExit(f"Expected /{repo}/blog/search/ in blog index")
    if 'href=/blog/posts/' in text or 'href=/blog/search/' in text:
        raise SystemExit(f"Found bare /blog/ links (missing /{repo}/ prefix)")


def validate_agent_ready(site_dir: Path) -> None:
    robots = site_dir / "robots.txt"
    sitemap = site_dir / "sitemap.xml"
    api_catalog = site_dir / ".well-known" / "api-catalog"
    skills_index = site_dir / ".well-known" / "agent-skills" / "index.json"

    for path in (robots, sitemap, api_catalog, skills_index):
        if not path.is_file():
            raise SystemExit(f"Missing {path}")

    robots_text = robots.read_text(encoding="utf-8")
    if "User-agent:" not in robots_text:
        raise SystemExit("robots.txt missing User-agent")
    if "Sitemap:" not in robots_text:
        raise SystemExit("robots.txt missing Sitemap")

    sitemap_text = sitemap.read_text(encoding="utf-8")
    if "index-en.html" not in sitemap_text:
        raise SystemExit("sitemap.xml should list index-en.html")
    for needle in ("resume.md", "resume.json", "llms.txt", "about-en.html"):
        if needle not in sitemap_text:
            raise SystemExit(f"sitemap.xml should list {needle}")

    for rel in ("about-en.html", "about-fr.html"):
        if not (site_dir / rel).is_file():
            raise SystemExit(f"Missing deploy artifact: {rel}")

    for rel in ("resume.md", "resume.json", "resume-fr.md", "resume-fr.json"):
        if not (site_dir / rel).is_file():
            raise SystemExit(f"Missing deploy artifact: {rel}")

    resume_json = site_dir / "resume.json"
    doc = json.loads(resume_json.read_text(encoding="utf-8"))
    if not (doc.get("basics") or {}).get("name"):
        raise SystemExit("resume.json missing basics.name")

    root = ET.parse(sitemap).getroot()
    if root.tag == q("sitemapindex"):
        raise SystemExit(
            "sitemap.xml is still a sitemapindex; run merge_root_sitemap.py before deploy"
        )
    if root.tag != q("urlset"):
        raise SystemExit(f"unexpected sitemap root: {root.tag!r}")

    catalog = json.loads(api_catalog.read_text(encoding="utf-8"))
    if "linkset" not in catalog or not isinstance(catalog["linkset"], list):
        raise SystemExit("api-catalog: expected top-level linkset array")

    skills_doc = json.loads(skills_index.read_text(encoding="utf-8"))
    for key in ("$schema", "skills"):
        if key not in skills_doc:
            raise SystemExit(f"agent-skills index missing {key!r}")
    for entry in skills_doc["skills"]:
        for k in ("name", "type", "description", "url", "sha256"):
            if k not in entry:
                raise SystemExit(f"agent-skills entry missing {k!r}: {entry!r}")

    for rel in (
        ".well-known/openid-configuration",
        ".well-known/oauth-authorization-server",
        ".well-known/oauth-protected-resource",
        ".well-known/mcp/server-card.json",
    ):
        p = site_dir / rel
        if not p.is_file():
            raise SystemExit(f"missing {rel}")
        json.loads(p.read_text(encoding="utf-8"))

    card = json.loads(
        (site_dir / ".well-known/mcp/server-card.json").read_text(encoding="utf-8")
    )
    if "serverInfo" not in card:
        raise SystemExit("mcp server-card missing serverInfo")


def validate_cv_pdfs(repo_root: Path) -> None:
    for rel in ("cv-en/resume.pdf", "cv-fr/resume.pdf"):
        path = repo_root / rel
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"Missing or empty {rel}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--site-dir",
        default="_site",
        help="Deploy output directory (default: _site)",
    )
    p.add_argument(
        "--repo",
        default="CV",
        help="GitHub repository name (Pages project path segment)",
    )
    p.add_argument(
        "--repo-root",
        default=".",
        help="Repository root for CV PDF checks (default: .)",
    )
    p.add_argument(
        "--skip-pdf-check",
        action="store_true",
        help="Skip cv-en/resume.pdf and cv-fr/resume.pdf presence check",
    )
    args = p.parse_args()

    site_dir = Path(args.site_dir).resolve()
    if not site_dir.is_dir():
        print(f"ERROR: site directory not found: {site_dir}", file=sys.stderr)
        return 1

    if not args.skip_pdf_check:
        validate_cv_pdfs(Path(args.repo_root).resolve())

    validate_blog_nav(site_dir, args.repo)
    validate_agent_ready(site_dir)
    print("Deploy artifact validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
