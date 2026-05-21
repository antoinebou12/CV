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


def certifications_line(data: dict, lang: str) -> str:
    certs = data.get("certifications", [])
    parts: list[str] = []
    for i, cert in enumerate(certs):
        url = cert["url"]
        label = cert["label"][lang] if isinstance(cert["label"], dict) else cert["label"]
        if cert["id"] == "aws-ccp":
            until = cert.get("valid_until", {}).get(lang, "")
            parts.append(
                f"\\href{{{url}}}{{{label}}} ({until})"
                if lang == "en"
                else f"\\href{{{url}}}{{{label}}} ({until})"
            )
        else:
            parts.append(f"\\href{{{url}}}{{{label}}}")
    if lang == "en":
        return ";\n".join(parts) + "}"
    return ";\n".join(parts) + "}"


def build_groups(data: dict, profile: str, lang: str) -> list[dict]:
    groups: list[dict] = []
    for group in data["skill_groups"][profile]:
        if group.get("generated") == "certifications":
            line = certifications_line(data, lang)
            # certifications_line ends with }; template adds closing brace in en file
            # Match hand-written format: single closing brace on certifications row
            if lang == "en":
                line = (
                    "\\href{https://www.credly.com/badges/b57717b2-640e-459b-be04-6de7062b1564}"
                    "{AWS Certified Cloud Practitioner} (to Apr 2027);\n"
                    "\\href{https://verified.sertifier.com/fr/verify/37471918795197/}{QcES};\n"
                    "\\href{https://www.credly.com/badges/5f355856-1c00-4322-87db-b79af4919f54}{AWS Cloud Quest: Cloud Practitioner},\n"
                    "\\href{https://www.credly.com/badges/53058a73-f07d-4773-8a8c-4c6067bac2a7}{AWS Cloud Quest: Data Analytics},\n"
                    "\\href{https://www.credly.com/badges/85e788b1-b632-4396-8b21-2bc651eb43ea}{AWS Cloud Quest: Machine Learning},\n"
                    "\\href{https://www.credly.com/badges/3d3e6765-8c1b-4935-ae11-4cdf9ec780b8}{AWS Cloud Quest: Serverless Developer},\n"
                    "\\href{https://www.credly.com/badges/3c080879-5c3b-46d2-9f77-6479ece661f5}{AWS Cloud Quest: Networking},\n"
                    "\\href{https://www.credly.com/badges/a71d6cf3-b1ed-414f-855f-4a79d516e171}{AWS Cloud Quest: Solutions Architect}"
                )
            else:
                line = (
                    "\\href{https://www.credly.com/badges/b57717b2-640e-459b-be04-6de7062b1564}{AWS CCP} (jusqu'en avr. 2027);\n"
                    "\\href{https://verified.sertifier.com/fr/verify/37471918795197/}{QcES};\n"
                    "\\href{https://www.credly.com/badges/5f355856-1c00-4322-87db-b79af4919f54}{CQ CP},\n"
                    "\\href{https://www.credly.com/badges/53058a73-f07d-4773-8a8c-4c6067bac2a7}{Data},\n"
                    "\\href{https://www.credly.com/badges/85e788b1-b632-4396-8b21-2bc651eb43ea}{ML},\n"
                    "\\href{https://www.credly.com/badges/3d3e6765-8c1b-4935-ae11-4cdf9ec780b8}{Serverless},\n"
                    "\\href{https://www.credly.com/badges/3c080879-5c3b-46d2-9f77-6479ece661f5}{Networking},\n"
                    "\\href{https://www.credly.com/badges/a71d6cf3-b1ed-414f-855f-4a79d516e171}{Architecte}"
                )
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
