#!/usr/bin/env python3
"""Render plain Markdown resumes from JSON Resume sources in data/."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT
DATA_DIR = REPO_ROOT / "data"

LOCALES = {
    "en": {
        "input": DATA_DIR / "resume.en.json",
        "output": REPO_ROOT / "resume.md",
        "contact": "Contact",
        "summary": "Summary",
        "experience": "Experience",
        "education": "Education",
        "skills": "Skills",
        "projects": "Selected projects",
        "certifications": "Certifications",
        "footer_html": "Interactive CV (HTML)",
        "footer_pdf": "PDF",
        "footer_md_other": "French Markdown",
        "footer_json": "JSON Resume",
        "footer_json_other": "French JSON",
        "present": "present",
    },
    "fr": {
        "input": DATA_DIR / "resume.fr.json",
        "output": REPO_ROOT / "resume-fr.md",
        "contact": "Coordonnées",
        "summary": "Profil",
        "experience": "Expérience",
        "education": "Formation",
        "skills": "Compétences",
        "projects": "Projets sélectionnés",
        "certifications": "Certifications",
        "footer_html": "CV interactif (HTML)",
        "footer_pdf": "PDF",
        "footer_md_other": "CV Markdown (anglais)",
        "footer_json": "JSON Resume",
        "footer_json_other": "JSON (anglais)",
        "present": "aujourd'hui",
    },
}


def format_dates(start: str | None, end: str | None, present: str) -> str:
    parts: list[str] = []
    if start:
        parts.append(start)
    if end:
        parts.append(end)
    elif start:
        parts.append(present)
    return " — ".join(parts) if parts else ""


def render(data: dict, labels: dict) -> str:
    meta = data.get("meta") or {}
    basics = data.get("basics") or {}
    lines: list[str] = []

    name = basics.get("name", "").strip()
    label = basics.get("label", "").strip()
    lines.append(f"# {name}")
    if label:
        lines.append("")
        lines.append(label)

    lines.extend(["", f"## {labels['contact']}"])
    if basics.get("email"):
        lines.append(f"- Email: {basics['email']}")
    if basics.get("phone"):
        lines.append(f"- Phone: {basics['phone']}")
    if basics.get("url"):
        lines.append(f"- Web: {basics['url']}")
    loc = basics.get("location") or {}
    loc_bits = [loc.get("city"), loc.get("region"), loc.get("countryCode")]
    loc_str = ", ".join(x for x in loc_bits if x)
    if loc_str:
        lines.append(f"- Location: {loc_str}")
    for profile in basics.get("profiles") or []:
        network = profile.get("network") or "Profile"
        url = profile.get("url") or ""
        if url:
            lines.append(f"- {network}: {url}")

    summary = (basics.get("summary") or "").strip()
    if summary:
        lines.extend(["", f"## {labels['summary']}", "", summary])

    work = data.get("work") or []
    if work:
        lines.extend(["", f"## {labels['experience']}"])
        for job in work:
            position = job.get("position") or ""
            company = job.get("name") or ""
            dates = format_dates(job.get("startDate"), job.get("endDate"), labels["present"])
            location = job.get("location") or ""
            header = f"### {position} @ {company}".strip()
            lines.append("")
            lines.append(header)
            meta_bits = [x for x in (dates, location) if x]
            if meta_bits:
                lines.append("")
                lines.append(" | ".join(meta_bits))
            for highlight in job.get("highlights") or []:
                lines.append(f"- {highlight}")

    education = data.get("education") or []
    if education:
        lines.extend(["", f"## {labels['education']}"])
        for edu in education:
            study = edu.get("studyType") or ""
            area = edu.get("area") or ""
            institution = edu.get("institution") or ""
            dates = format_dates(edu.get("startDate"), edu.get("endDate"), labels["present"])
            lines.append("")
            lines.append(f"### {study}, {area} — {institution}".strip(" ,"))
            if dates:
                lines.append("")
                lines.append(dates)
            for course in edu.get("courses") or []:
                lines.append(f"- {course}")

    skills = data.get("skills") or []
    if skills:
        lines.extend(["", f"## {labels['skills']}"])
        for group in skills:
            name = group.get("name") or "Skills"
            keywords = group.get("keywords") or []
            if keywords:
                lines.append(f"- **{name}:** {', '.join(keywords)}")

    projects = data.get("projects") or []
    if projects:
        lines.extend(["", f"## {labels['projects']}"])
        for project in projects:
            pname = project.get("name") or "Project"
            url = project.get("url") or ""
            desc = (project.get("description") or "").strip()
            lines.append("")
            if url:
                lines.append(f"### [{pname}]({url})")
            else:
                lines.append(f"### {pname}")
            if desc:
                lines.append("")
                lines.append(desc)

    certs = data.get("certificates") or []
    if certs:
        lines.extend(["", f"## {labels['certifications']}"])
        for cert in certs:
            cname = cert.get("name") or ""
            url = cert.get("url") or ""
            if url:
                lines.append(f"- [{cname}]({url})")
            elif cname:
                lines.append(f"- {cname}")

    lines.extend(["", "---", ""])
    locale = meta.get("locale", "en")
    if locale == "en":
        lines.append(
            f"{labels['footer_html']}: {meta.get('htmlCv', basics.get('url', ''))} | "
            f"{labels['footer_pdf']}: {meta.get('pdfCv', '')}"
        )
        lines.append(
            f"{labels['footer_md_other']}: {meta.get('markdownCvFr', '')} | "
            f"{labels['footer_json']}: {meta.get('siteRoot', '')}/resume.json | "
            f"{labels['footer_json_other']}: {meta.get('jsonCvFr', '')}"
        )
    else:
        lines.append(
            f"{labels['footer_html']}: {meta.get('htmlCv', basics.get('url', ''))} | "
            f"{labels['footer_pdf']}: {meta.get('pdfCv', '')}"
        )
        lines.append(
            f"{labels['footer_md_other']}: {meta.get('markdownCvEn', '')} | "
            f"{labels['footer_json']}: {meta.get('jsonCvEn', '')} | "
            f"{labels['footer_json_other']}: {meta.get('siteRoot', '')}/resume-fr.json"
        )

    return "\n".join(lines).rstrip() + "\n"


def render_locale(locale: str) -> Path:
    cfg = LOCALES[locale]
    data = json.loads(cfg["input"].read_text(encoding="utf-8"))
    out = cfg["output"]
    out.write_text(render(data, LOCALES[locale]), encoding="utf-8", newline="\n")
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--locale", choices=sorted(LOCALES), help="Render one locale")
    p.add_argument("--all", action="store_true", help="Render en and fr")
    args = p.parse_args()

    if not args.all and not args.locale:
        p.error("Specify --locale or --all")

    locales = sorted(LOCALES) if args.all else [args.locale]
    for locale in locales:
        try:
            path = render_locale(locale)
        except FileNotFoundError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
