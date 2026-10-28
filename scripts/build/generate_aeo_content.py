#!/usr/bin/env python3
"""Patch CV HTML pages from data/aeo.yaml (lead, freshness, nav)."""
from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT, script_path
AEO_PATH = REPO_ROOT / "data" / "aeo.yaml"
# Path-relative: localhost/127.0.0.1 → same-origin /blog/; production under /CV/ → /CV/blog/.
BLOG_NAV_HREF = "blog/"

LEAD_BEGIN = "<!-- AEO_LEAD:BEGIN -->"
LEAD_END = "<!-- AEO_LEAD:END -->"
FRESHNESS_BEGIN = "<!-- AEO_FRESHNESS:BEGIN -->"
FRESHNESS_END = "<!-- AEO_FRESHNESS:END -->"
UPDATED_BEGIN = "<!-- CV_LAST_UPDATED:BEGIN -->"
UPDATED_END = "<!-- CV_LAST_UPDATED:END -->"

LOCALES = {
    "en": {
        "cv": REPO_ROOT / "index-en.html",
        "lang": "en",
        "blog_nav": "Blog",
        "last_updated_label": "Last updated",
        "date_locale": "en_CA",
    },
    "fr": {
        "cv": REPO_ROOT / "index-fr.html",
        "lang": "fr",
        "blog_nav": "Blog",
        "last_updated_label": "Dernière mise à jour",
        "date_locale": "fr_CA",
    },
}


def load_aeo() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required (pip install pyyaml)")
    return yaml.safe_load(AEO_PATH.read_text(encoding="utf-8"))


def iso_modified(date_str: str) -> str:
    return f"{date_str}T12:00:00+00:00"


def format_display_date(date_str: str, locale: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    if locale.startswith("fr"):
        months = (
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        )
        return f"{dt.day} {months[dt.month - 1]} {dt.year}"
    return dt.strftime("%d %B %Y")


def esc(text: str) -> str:
    return html.escape(text.strip(), quote=True)


def lang_text(block: dict | None, lang: str) -> str:
    if not block:
        return ""
    if isinstance(block, str):
        return block.strip()
    return (block.get(lang) or "").strip()


def freshness_meta_block(last: str, published: str) -> str:
    mod = iso_modified(last)
    pub = iso_modified(published)
    return (
        f"{FRESHNESS_BEGIN}\n"
        f'  <meta property="article:modified_time" content="{mod}">\n'
        f'  <meta property="article:published_time" content="{pub}">\n'
        f"{FRESHNESS_END}"
    )


def lead_block(lead: str) -> str:
    text = esc(" ".join(lead.split()))
    return (
        f"{LEAD_BEGIN}\n"
        f'    <p class="aeo-about-intro aeo-lead aeo-agent-only">{text}</p>\n'
        f"{LEAD_END}"
    )


def last_updated_block(locale: str, last: str) -> str:
    cfg = LOCALES[locale]
    display = format_display_date(last, cfg["date_locale"])
    label = cfg["last_updated_label"]
    return (
        f"{UPDATED_BEGIN}\n"
        f'    <p class="cv-last-updated">{esc(label)}: '
        f'<time datetime="{last}">{display}</time></p>\n'
        f"{UPDATED_END}"
    )


def cv_nav_block(locale: str) -> str:
    cfg = LOCALES[locale]
    nav_aria = "Site and language" if locale == "en" else "Site et langue"
    lang_aria = "Language" if locale == "en" else "Langue"
    en_current = ' class="current"' if locale == "en" else ""
    fr_current = ' class="current"' if locale == "fr" else ""
    return f"""  <nav class="cv-site-nav" aria-label="{nav_aria}">
    <a class="cv-nav-pill cv-nav-blog" href="{BLOG_NAV_HREF}">{cfg["blog_nav"]}</a>
    <div class="cv-nav-pill cv-nav-lang" aria-label="{lang_aria}">
      <a href="index-en.html"{en_current}>EN</a><span class="sep" aria-hidden="true"> | </span><a href="index-fr.html"{fr_current}>FR</a>
    </div>
  </nav>"""


def replace_block(html: str, begin: str, end: str, new: str) -> str:
    pattern = re.compile(rf"{re.escape(begin)}.*?{re.escape(end)}", re.DOTALL)
    if pattern.search(html):
        return pattern.sub(new, html, count=1)
    return html


def strip_about_page_links(html: str) -> str:
    """Remove leftover links to deleted about-*.html pages."""
    html = re.sub(
        r'\s*<a href="about-(?:en|fr)\.html"[^>]*>.*?</a>\s*',
        "\n",
        html,
        count=2,
    )
    html = re.sub(
        r'\s*<a href="about-(?:en|fr)\.html"[^>]*>.*?</a>',
        "",
        html,
    )
    return html


def patch_cv(locale: str, aeo: dict) -> None:
    cfg = LOCALES[locale]
    path = cfg["cv"]
    html = path.read_text(encoding="utf-8")
    lang = cfg["lang"]
    lead = lang_text(aeo.get("lead"), lang)
    last = aeo.get("lastUpdated", "2026-08-01")
    published = aeo.get("datePublished", "2024-06-01")
    html = strip_about_page_links(html)

    if "cv-aeo.css" not in html:
        html = html.replace(
            '<link rel="stylesheet" href="css/cv-print.css" media="print">',
            '<link rel="stylesheet" href="css/cv-aeo.css">\n'
            '  <link rel="stylesheet" href="css/cv-print.css" media="print">',
            1,
        )

    fresh = freshness_meta_block(last, published)
    if FRESHNESS_BEGIN in html:
        html = replace_block(html, FRESHNESS_BEGIN, FRESHNESS_END, fresh)
    else:
        html = html.replace("</title>", f"</title>\n{fresh}", 1)

    nav_new = cv_nav_block(locale)
    skip_nav_pat = re.compile(
        r'(<a class="skip-link"[^>]*>.*?</a>)\s*<nav class="cv-site-nav"[^>]*>.*?</nav>',
        re.DOTALL,
    )
    html = skip_nav_pat.sub(rf"\1\n{nav_new}", html, count=1)

    lead_new = lead_block(lead) if lead.strip() else ""
    if LEAD_BEGIN in html and UPDATED_BEGIN in html:
        if lead_new:
            html = replace_block(html, LEAD_BEGIN, LEAD_END, lead_new)
        else:
            html = replace_block(html, LEAD_BEGIN, LEAD_END, "")
    elif lead_new:
        if UPDATED_BEGIN in html:
            html = html.replace(UPDATED_BEGIN, f"{lead_new}\n{UPDATED_BEGIN}", 1)
        else:
            html = html.replace("  </main>", f"{lead_new}\n  </main>", 1)

    updated = last_updated_block(locale, last)
    if UPDATED_BEGIN in html:
        html = replace_block(html, UPDATED_BEGIN, UPDATED_END, updated)
    else:
        html = html.replace("  </main>", f"{updated}\n  </main>", 1)

    html = re.sub(r"\n{4,}(?=<!-- AEO_LEAD:BEGIN -->)", "\n\n", html)

    path.write_text(html, encoding="utf-8", newline="\n")
    print(f"Updated {path}")


def process_locale(locale: str, aeo: dict) -> None:
    patch_cv(locale, aeo)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--locale", choices=sorted(LOCALES))
    p.add_argument("--all", action="store_true")
    args = p.parse_args()
    if not args.all and not args.locale:
        p.error("Specify --locale or --all")
    try:
        aeo = load_aeo()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    locales = sorted(LOCALES) if args.all else [args.locale]
    for loc in locales:
        process_locale(loc, aeo)
    if "en" in locales:
        import subprocess

        sync = script_path("html", "sync_index_html.py")
        subprocess.run([sys.executable, str(sync)], cwd=REPO_ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
