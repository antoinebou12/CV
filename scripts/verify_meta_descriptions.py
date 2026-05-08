"""Verify meta / og:description / twitter:description lengths (50-160 runes) for key static HTML and Hugo build output."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC_FILES = [
    ROOT / "index.html",
    ROOT / "index-en.html",
    ROOT / "index-fr.html",
    ROOT / "404.html",
    ROOT / "linktree" / "index.html",
]

def _first_group(html: str, patterns: tuple[re.Pattern[str], ...]) -> str:
    for pat in patterns:
        m = pat.search(html)
        if m:
            return m.group(1)
    return ""


# Minified Hugo uses unquoted attribute names; static CV pages use quoted names.
META_PATTERNS = (
    re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I),
    re.compile(r"<meta\s+name=description\s+content=\"([^\"]*)\"", re.I),
)
OG_PATTERNS = (
    re.compile(r'<meta\s+property="og:description"\s+content="([^"]*)"', re.I),
    re.compile(r"<meta\s+property=og:description\s+content=\"([^\"]*)\"", re.I),
)
TW_PATTERNS = (
    re.compile(r'<meta\s+name="twitter:description"\s+content="([^"]*)"', re.I),
    re.compile(r"<meta\s+name=twitter:description\s+content=\"([^\"]*)\"", re.I),
)


def extract(html: str) -> dict[str, str]:
    return {
        "meta": _first_group(html, META_PATTERNS),
        "og": _first_group(html, OG_PATTERNS),
        "twitter": _first_group(html, TW_PATTERNS),
    }


def check_file(path: Path, require_twitter: bool) -> list[str]:
    errs: list[str] = []
    html = path.read_text(encoding="utf-8")
    d = extract(html)
    for label, text in d.items():
        if label == "twitter" and not require_twitter:
            continue
        if label == "twitter" and not text.strip():
            errs.append(f"{path.name}: missing twitter:description")
            continue
        n = len(text)
        if n < 50 or n > 160:
            errs.append(f"{path.name}: {label} length {n} (want 50-160): {text[:80]!r}…")
    if d["meta"] and d["og"] and d["meta"] != d["og"]:
        errs.append(f"{path.name}: meta description != og:description")
    if require_twitter and d["twitter"] and d["meta"] != d["twitter"]:
        errs.append(f"{path.name}: meta description != twitter:description")
    return errs


def main() -> int:
    errs: list[str] = []
    for p in STATIC_FILES:
        if not p.is_file():
            errs.append(f"missing {p.relative_to(ROOT)}")
            continue
        tw = p.name != "404.html"
        errs.extend(check_file(p, require_twitter=tw))

    out = ROOT / "_site_hugo_test"
    hugo_dir = ROOT / "hugo"
    hugo_env = {**os.environ, "HUGO_ENV": "production"}
    subprocess.run(
        [
            "hugo",
            "--gc",
            "--minify",
            "-s",
            str(hugo_dir),
            "-d",
            str(out),
            "-b",
            "https://antoineboucher.info/CV/blog/",
        ],
        cwd=ROOT,
        check=True,
        env=hugo_env,
    )

    samples = [
        out / "index.html",
        out / "posts" / "caddy-ec2-cloudwatch-lambda" / "index.html",
        out / "tags" / "index.html",
        out / "tags" / "aws" / "index.html",
        out / "projects" / "index.html",
        out / "search" / "index.html",
        out / "fr" / "tags" / "index.html",
        out / "fr" / "tags" / "aws" / "index.html",
    ]
    for p in samples:
        if not p.is_file():
            errs.append(f"missing build sample {p.relative_to(ROOT)}")
            continue
        html = p.read_text(encoding="utf-8")
        d = extract(html)
        for label, text in d.items():
            if not text.strip():
                errs.append(f"{p.relative_to(ROOT)}: empty {label} description")
                continue
            n = len(text)
            if n < 50 or n > 160:
                errs.append(
                    f"{p.relative_to(ROOT)}: {label} length {n} (want 50-160)"
                )
        if d["meta"] and d["og"] and d["meta"] != d["og"]:
            errs.append(f"{p.relative_to(ROOT)}: meta != og")
        if d["meta"] and d["twitter"] and d["meta"] != d["twitter"]:
            errs.append(f"{p.relative_to(ROOT)}: meta != twitter")

    if errs:
        print("FAILURES:")
        for e in errs:
            print(" ", e)
        return 1
    print("All meta description checks passed (static + Hugo samples).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
