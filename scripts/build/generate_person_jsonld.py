#!/usr/bin/env python3
"""Generate Schema.org Person JSON-LD and inject into CV HTML pages."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT
DATA_DIR = REPO_ROOT / "data"
AEO_PATH = DATA_DIR / "aeo.yaml"

SITE_ROOT = "https://antoineboucher.info/CV"
CAL_COM = "https://cal.com/antoine-boucher-dev/30min"
IMAGE = f"{SITE_ROOT}/antoine.png"

HREFLANG_BLOCK = """  <link rel="alternate" hreflang="en" href="https://antoineboucher.info/CV/index-en.html" />
  <link rel="alternate" hreflang="fr" href="https://antoineboucher.info/CV/index-fr.html" />
  <link rel="alternate" hreflang="x-default" href="https://antoineboucher.info/CV/index-en.html" />"""

JSONLD_BEGIN = "<!-- PERSON_JSONLD:BEGIN -->"
JSONLD_END = "<!-- PERSON_JSONLD:END -->"

LOCALE_PAGES = {
    "en": {
        "data": DATA_DIR / "resume.en.json",
        "html": REPO_ROOT / "index-en.html",
        "page_url": f"{SITE_ROOT}/index-en.html",
        "lang": "en",
    },
    "fr": {
        "data": DATA_DIR / "resume.fr.json",
        "html": REPO_ROOT / "index-fr.html",
        "page_url": f"{SITE_ROOT}/index-fr.html",
        "lang": "fr",
    },
}


# Phrases models often match beyond flat skill keywords (no marketing fluff).
EXTRA_KNOWS_ABOUT: tuple[str, ...] = (
    "DevSecOps",
    "GitLab CI/CD",
    "Kubernetes",
    "Terraform",
    "UML",
    "Model Context Protocol",
)


def flatten_knows_about(data: dict) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for phrase in EXTRA_KNOWS_ABOUT:
        if phrase not in seen:
            seen.add(phrase)
            out.append(phrase)
    for group in data.get("skills") or []:
        for kw in group.get("keywords") or []:
            k = kw.strip()
            if k and k not in seen:
                seen.add(k)
                out.append(k)
    return out


def current_employers(work: list[dict]) -> list[dict]:
    orgs: list[dict] = []
    for job in work:
        if job.get("endDate"):
            continue
        name = job.get("name")
        if not name:
            continue
        org: dict = {"@type": "Organization", "name": name}
        if job.get("url"):
            org["url"] = job["url"]
        orgs.append(org)
    return orgs


def alumni_orgs(education: list[dict]) -> list[dict]:
    orgs: list[dict] = []
    seen: set[str] = set()
    for edu in education:
        name = edu.get("institution")
        if not name or name in seen:
            continue
        seen.add(name)
        org: dict = {"@type": "EducationalOrganization", "name": name}
        if edu.get("url"):
            org["url"] = edu["url"]
        orgs.append(org)
    return orgs


def project_nodes(projects: list[dict]) -> list[dict]:
    nodes: list[dict] = []
    for i, project in enumerate(projects[:6], start=1):
        pid = f"#project-{i}"
        node: dict = {
            "@type": "SoftwareSourceCode",
            "@id": pid,
            "name": project.get("name") or "Project",
        }
        if project.get("url"):
            node["codeRepository"] = project["url"]
            node["url"] = project["url"]
        if project.get("description"):
            node["description"] = project["description"]
        if project.get("keywords"):
            node["keywords"] = ", ".join(project["keywords"])
        nodes.append(node)
    return nodes


def load_aeo_dates() -> tuple[str, str]:
    """Return (dateModified, datePublished) as YYYY-MM-DD."""
    if yaml is None or not AEO_PATH.is_file():
        return "2026-08-01", "2024-06-01"
    aeo = yaml.safe_load(AEO_PATH.read_text(encoding="utf-8")) or {}
    return aeo.get("lastUpdated", "2026-08-01"), aeo.get(
        "datePublished", "2024-06-01"
    )


def iso_date(date_str: str) -> str:
    return f"{date_str}T12:00:00+00:00"


def build_graph(data: dict, page_url: str, lang: str) -> dict:
    basics = data.get("basics") or {}
    name = basics.get("name") or "Antoine Boucher"
    label = basics.get("label") or ""
    description = (basics.get("summary") or "").strip()

    same_as: list[str] = []
    for profile in basics.get("profiles") or []:
        url = profile.get("url")
        if url and url not in same_as:
            same_as.append(url)
    if CAL_COM not in same_as:
        same_as.append(CAL_COM)

    person_id = f"{page_url}#person"
    webpage_id = f"{page_url}#webpage"
    website_id = f"{SITE_ROOT}/#website"
    about_url = f"{SITE_ROOT}/about-{lang}.html"
    about_id = f"{about_url}#webpage"
    last_mod, date_pub = load_aeo_dates()

    person: dict = {
        "@type": "Person",
        "@id": person_id,
        "name": name,
        "url": page_url,
        "image": IMAGE,
        "sameAs": same_as,
    }
    if label:
        person["jobTitle"] = label
    if description:
        person["description"] = description

    knows = flatten_knows_about(data)
    if knows:
        person["knowsAbout"] = knows

    alumni = alumni_orgs(data.get("education") or [])
    if alumni:
        person["alumniOf"] = alumni if len(alumni) > 1 else alumni[0]

    employers = current_employers(data.get("work") or [])
    if employers:
        person["worksFor"] = employers if len(employers) > 1 else employers[0]

    projects = project_nodes(data.get("projects") or [])
    website: dict = {
        "@type": "WebSite",
        "@id": website_id,
        "url": f"{SITE_ROOT}/",
        "name": f"{name} — CV",
        "publisher": {"@id": person_id},
    }
    if description:
        website["description"] = description

    webpage: dict = {
        "@type": "WebPage",
        "@id": webpage_id,
        "url": page_url,
        "name": f"{name} — CV ({'English' if lang == 'en' else 'français'})",
        "description": description
        or (
            "Interactive English HTML resume: platform, graphics, Rust, cloud; PDF, blog, and open-source links."
            if lang == "en"
            else "CV HTML interactif : plateforme, infographie, Rust, nuage ; PDF, blog et dépôts open source."
        ),
        "inLanguage": lang,
        "dateModified": iso_date(last_mod),
        "datePublished": iso_date(date_pub),
        "isPartOf": {"@id": website_id},
        "mainEntity": {"@id": person_id},
        "about": {"@id": about_id},
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".aeo-lead"],
        },
    }
    website["inLanguage"] = ["en", "fr"]

    graph: list[dict] = [website, webpage, person]

    if projects:
        for node in projects:
            graph.append(node)
        person["subjectOf"] = [{"@id": n["@id"]} for n in projects]

    return {"@context": "https://schema.org", "@graph": graph}


def jsonld_script_block(graph: dict) -> str:
    payload = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    return (
        f"{JSONLD_BEGIN}\n"
        f'  <script type="application/ld+json">\n{payload}\n'
        f"  </script>\n"
        f"{JSONLD_END}"
    )


def inject_jsonld(html: str, block: str) -> str:
    pattern = re.compile(
        rf"{re.escape(JSONLD_BEGIN)}.*?{re.escape(JSONLD_END)}",
        re.DOTALL,
    )
    if pattern.search(html):
        return pattern.sub(block, html, count=1)
    # Legacy single-line script fallback
    legacy = re.compile(
        r'\s*<script type="application/ld\+json">\s*\{.*?\}\s*</script>',
        re.DOTALL,
    )
    if legacy.search(html):
        return legacy.sub("\n" + block, html, count=1)
    raise ValueError("No JSON-LD anchor or legacy script found in HTML")


def inject_hreflang(html: str) -> str:
    if 'hreflang="en"' in html:
        return html
    canonical_m = re.search(r'(<link rel="canonical"[^>]*>)', html)
    if canonical_m:
        insert_at = canonical_m.end()
        return html[:insert_at] + "\n" + HREFLANG_BLOCK + html[insert_at:]
    title_m = re.search(r"</title>", html)
    if title_m:
        return html[: title_m.end()] + "\n" + HREFLANG_BLOCK + html[title_m.end() :]
    raise ValueError("Could not find insertion point for hreflang links")


def patch_index_html_legacy() -> None:
    path = REPO_ROOT / "index.html"
    if not path.is_file():
        return
    html = path.read_text(encoding="utf-8")
    changed = False
    if 'rel="canonical"' not in html:
        snippet = (
            '  <link rel="canonical" href="https://antoineboucher.info/CV/index-en.html">\n'
        )
        html = html.replace("</title>", "</title>\n" + snippet, 1)
        changed = True
    if 'hreflang="en"' not in html:
        html = inject_hreflang(html)
        changed = True
    if changed:
        path.write_text(html, encoding="utf-8", newline="\n")
        print(f"Updated {path}")


def process_locale(locale: str) -> None:
    cfg = LOCALE_PAGES[locale]
    data = json.loads(cfg["data"].read_text(encoding="utf-8"))
    graph = build_graph(data, cfg["page_url"], cfg["lang"])
    block = jsonld_script_block(graph)
    html_path: Path = cfg["html"]
    html = html_path.read_text(encoding="utf-8")
    html = inject_jsonld(html, block)
    html = inject_hreflang(html)
    html_path.write_text(html, encoding="utf-8", newline="\n")
    print(f"Updated {html_path}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--locale", choices=sorted(LOCALE_PAGES), help="Patch one HTML page")
    p.add_argument("--all", action="store_true", help="Patch en, fr, and legacy index.html")
    args = p.parse_args()

    if not args.all and not args.locale:
        p.error("Specify --locale or --all")

    locales = sorted(LOCALE_PAGES) if args.all else [args.locale]
    for locale in locales:
        try:
            process_locale(locale)
        except (FileNotFoundError, ValueError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
    if args.all:
        patch_index_html_legacy()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
