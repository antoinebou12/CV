"""Locale-aware spellcheck: codespell (EN) and aspell (FR).

Used by .github/workflows/quality.yml and pre-commit.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from collections.abc import Iterable, Iterator
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT

CODE_SPELL_IGNORE = REPO_ROOT / ".codespell-ignore-words"
ASPELL_FR_PWS = REPO_ROOT / ".aspell.fr.pws"

EN_STATIC = (
    "index-en.html",
    "about-en.html",
    "index.html",
    "404.html",
    "AGENTS.md",
)

FR_STATIC = (
    "index-fr.html",
    "about-fr.html",
)

EN_DIRS = ("cv-en/latex", "letters/en", "docs", "scripts")
FR_DIRS = ("cv-fr/latex", "letters/fr")

EN_DATA = ("data/resume.en.json",)
FR_DATA = ("data/resume.fr.json",)


def _exists(path: Path) -> bool:
    return path.is_file() or path.is_dir()


def _hugo_markdown(lang: str) -> Iterator[Path]:
    content = REPO_ROOT / "hugo" / "content"
    if not content.is_dir():
        return
    for path in sorted(content.rglob("*.md")):
        is_fr = path.name.endswith(".fr.md") or path.name == "search.fr.md"
        if lang == "fr" and is_fr:
            yield path
        elif lang == "en" and not is_fr:
            yield path


def collect_paths(lang: str) -> list[Path]:
    paths: list[Path] = []
    if lang == "en":
        for rel in EN_STATIC + EN_DATA:
            p = REPO_ROOT / rel
            if _exists(p):
                paths.append(p)
        for rel in EN_DIRS:
            p = REPO_ROOT / rel
            if p.is_dir():
                paths.extend(sorted(p.rglob("*")))
        paths.extend(_hugo_markdown("en"))
    else:
        for rel in FR_STATIC + FR_DATA:
            p = REPO_ROOT / rel
            if _exists(p):
                paths.append(p)
        for rel in FR_DIRS:
            p = REPO_ROOT / rel
            if p.is_dir():
                paths.extend(sorted(p.rglob("*")))
        paths.extend(_hugo_markdown("fr"))

    out: list[Path] = []
    seen: set[Path] = set()
    for p in paths:
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".html", ".md", ".tex", ".json", ".py", ".ps1", ".yaml", ".yml"}:
            continue
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        out.append(p)
    return out


def _aspell_mode(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".html", ".md"}:
        return "markdown" if ext == ".md" else "html"
    if ext == ".tex":
        return "tex"
    return "none"


def run_codespell(paths: list[Path]) -> list[str]:
    if not paths:
        return []
    codespell = shutil.which("codespell")
    if not codespell:
        return ["codespell not found on PATH (pip install codespell)"]

    cmd = [
        codespell,
        "--ignore-words",
        str(CODE_SPELL_IGNORE),
        *[str(p.relative_to(REPO_ROOT)) for p in paths],
    ]
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if proc.returncode == 0:
        return []
    detail = (proc.stdout or proc.stderr or "").strip()
    return [detail or "codespell reported spelling issues"]


def run_aspell_fr(paths: list[Path]) -> list[str]:
    if not paths:
        return []
    aspell = shutil.which("aspell")
    if not aspell:
        return ["aspell not found on PATH (install aspell and aspell-fr)"]

    personal = ["-p", str(ASPELL_FR_PWS)] if ASPELL_FR_PWS.is_file() else []
    errors: list[str] = []

    for path in paths:
        rel = path.relative_to(REPO_ROOT)
        mode = _aspell_mode(path)
        cmd = [
            aspell,
            "--lang=fr",
            "--encoding=utf-8",
            f"--mode={mode}",
            "list",
            *personal,
        ]
        text = path.read_text(encoding="utf-8")
        proc = subprocess.run(
            cmd,
            input=text,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0 and proc.stderr:
            errors.append(f"{rel}: aspell failed: {proc.stderr.strip()}")
            continue
        words = [
            line.strip()
            for line in (proc.stdout or "").splitlines()
            if line.strip() and not line.startswith("*")
        ]
        if words:
            sample = ", ".join(words[:12])
            extra = f" (+{len(words) - 12} more)" if len(words) > 12 else ""
            errors.append(f"{rel}: {sample}{extra}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lang",
        choices=("en", "fr", "all"),
        default="all",
        help="Run only English, only French, or both (default).",
    )
    args = parser.parse_args()

    failures: list[str] = []

    if args.lang in ("en", "all"):
        en_paths = collect_paths("en")
        failures.extend(run_codespell(en_paths))

    if args.lang in ("fr", "all"):
        fr_paths = collect_paths("fr")
        failures.extend(run_aspell_fr(fr_paths))

    if failures:
        print("Spellcheck FAILED:")
        for item in failures:
            print(item)
        return 1

    langs = []
    if args.lang in ("en", "all"):
        langs.append(f"EN codespell ({len(collect_paths('en'))} files)")
    if args.lang in ("fr", "all"):
        langs.append(f"FR aspell ({len(collect_paths('fr'))} files)")
    print("Spellcheck OK:", ", ".join(langs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
