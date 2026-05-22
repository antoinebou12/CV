"""Generate LaTeX (and future HTML) from data/cv.yaml."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

_BUILD = Path(__file__).resolve().parent
_SCRIPTS = _BUILD.parent
if str(_BUILD) not in sys.path:
    sys.path.insert(0, str(_BUILD))
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT
from skill_urls import LATEX_LINK_ORDER, SKILL_URLS

ROOT = REPO_ROOT
DATA = ROOT / "data" / "cv.yaml"
TEMPLATES = ROOT / "templates"

SECTION_TITLES = {"en": "Competences", "fr": "Compétences"}

_SEGMENT_SPLIT = re.compile(r"(, | · )")


_HREF_CHUNK = re.compile(r"(\\href\{[^}]*\}\{[^}]*\})")


def _split_href_chunks(text: str) -> list[str]:
    return _HREF_CHUNK.split(text)


def linkify_segment(segment: str) -> str:
    if "\\href{" in segment:
        return segment
    core = segment.strip()
    if not core:
        return segment
    prefix = segment[: len(segment) - len(segment.lstrip())]
    suffix = segment[len(segment.rstrip()) :]

    if core in SKILL_URLS:
        url = SKILL_URLS[core]
        return f"{prefix}\\href{{{url}}}{{{core}}}{suffix}"

    updated = core
    for label in LATEX_LINK_ORDER:
        url = SKILL_URLS[label]
        wrapped = f"\\href{{{url}}}{{{label}}}"
        if label not in updated or wrapped in updated:
            continue
        pieces = _split_href_chunks(updated)
        updated = "".join(
            piece if piece.startswith("\\href{") else piece.replace(label, wrapped)
            for piece in pieces
        )
    return prefix + updated + suffix


def linkify_latex_line(line: str) -> str:
    parts = _SEGMENT_SPLIT.split(line)
    return "".join(
        part if _SEGMENT_SPLIT.fullmatch(part) or "\\href{" in part else linkify_segment(part)
        for part in parts
    )


def load_data() -> dict:
    return yaml.safe_load(DATA.read_text(encoding="utf-8"))


def _cert_label(cert: dict, lang: str) -> str:
    label = cert["label"]
    if isinstance(label, dict):
        return label[lang]
    return label


def _cert_href(cert: dict, lang: str) -> str:
    url = cert["url"]
    label = _cert_label(cert, lang)
    if cert["id"] == "aws-ccp":
        until = cert.get("valid_until", {}).get(lang, "")
        return f"\\href{{{url}}}{{{label}}} ({until})"
    return f"\\href{{{url}}}{{{label}}}"


def format_certifications_latex(data: dict, lang: str) -> str:
    certs = data.get("certifications", [])
    by_id = {c["id"]: c for c in certs}
    line1_parts: list[str] = []
    if "aws-ccp" in by_id:
        line1_parts.append(_cert_href(by_id["aws-ccp"], lang))
    if "qces" in by_id:
        line1_parts.append(_cert_href(by_id["qces"], lang))
    line1 = "; ".join(line1_parts)

    cq_prefix = "Cloud Quest: " if lang == "en" else "Parcours Cloud Quest : "
    cq_links = [
        _cert_href(c, lang)
        for c in certs
        if c["id"].startswith("cq-")
    ]
    line2 = cq_prefix + ", ".join(cq_links)
    return f"{line1}; {line2}"


def build_groups(data: dict, profile: str, lang: str) -> list[dict]:
    groups: list[dict] = []
    for group in data["skill_groups"][profile]:
        if group.get("generated") == "certifications":
            line = format_certifications_latex(data, lang)
        else:
            line = linkify_latex_line(group["latex_line"])
        groups.append({"category": group["category"], "line": line})
    return groups


def render_skills(data: dict, lang: str) -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES / "latex"),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tpl = env.get_template("skills.tex.j2")
    profile = f"latex_{lang}"
    return tpl.render(
        section_title=SECTION_TITLES[lang],
        groups=build_groups(data, profile, lang),
    )


def write_outputs(data: dict) -> list[Path]:
    written: list[Path] = []
    for lang, sub in (("en", "cv-en"), ("fr", "cv-fr")):
        out = ROOT / sub / "latex" / "skills.tex"
        text = render_skills(data, lang)
        normalized = text.replace("\r\n", "\n")
        if not normalized.endswith("\n"):
            normalized += "\n"
        out.write_text(normalized, encoding="utf-8", newline="\n")
        written.append(out)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Regenerate and fail if skills.tex content would change",
    )
    args = parser.parse_args()

    if not DATA.is_file():
        print(f"Missing {DATA}")
        return 1

    data = load_data()
    before = {p: p.read_text(encoding="utf-8") if p.is_file() else "" for p in [
        ROOT / "cv-en" / "latex" / "skills.tex",
        ROOT / "cv-fr" / "latex" / "skills.tex",
    ]}

    written = write_outputs(data)

    if args.check:
        changed = [p for p in written if p.read_text(encoding="utf-8") != before[p]]
        if changed:
            print("generate_cv.py --check FAILED: skills.tex out of date. Run:")
            print("  python scripts/build/generate_cv.py")
            for p in written:
                if p.read_text(encoding="utf-8") != before[p]:
                    print(f"  changed: {p.relative_to(ROOT)}")
            return 1
        print("generate_cv.py --check passed.")
        return 0

    for p in written:
        print(f"Wrote {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
