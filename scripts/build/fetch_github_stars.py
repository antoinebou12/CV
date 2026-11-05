#!/usr/bin/env python3
"""Fetch the repositories starred by a GitHub account and group them by theme.

The blog page at /stars/ reads hugo/data/github_stars.json. GitHub only exposes the
starred list through the users/{login}/starred endpoint, which needs an authenticated
`gh` session (any scope). Run from the repository root:

    python scripts/build/fetch_github_stars.py            # uses `gh api`
    python scripts/build/fetch_github_stars.py --from stars.json   # reuse an export

Export without this script: gh api users/antoinebou12/starred --paginate > stars.json

Categories come from topics, primary language and description keywords (rules below),
so a repository can appear in two themes; the first match is its primary theme. The
script also writes hugo/content/stars/_index.md and _index.fr.md so the section only
exists once data does.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "hugo" / "data" / "github_stars.json"
CONTENT = ROOT / "hugo" / "content" / "stars"
LOGIN = "antoinebou12"

# Ordered: the first matching theme becomes the primary one.
THEMES = [
    ("ai", ["AI, LLMs & agents", "IA, LLM et agents"],
     r"\b(llm|gpt|openai|anthropic|claude|langchain|agent|mcp|model[- ]context|rag|embedding|transformer|diffusion|stable[- ]diffusion|comfyui|whisper|ollama|hugging ?face|machine[- ]learning|deep[- ]learning|neural|pytorch|tensorflow|prompt)\b"),
    ("graphics", ["Graphics, 3D & simulation", "Graphisme, 3D et simulation"],
     r"\b(opengl|vulkan|webgpu|wgpu|shader|render|blender|mitsuba|three\.?js|mesh|3d|geometry|physics|simulation|ray ?tracing|gltf|usd|point ?cloud|slam|photogrammetry|metrology|cad)\b"),
    ("diagrams", ["Diagrams & documentation", "Diagrammes et documentation"],
     r"\b(mermaid|plantuml|kroki|diagram|d2|graphviz|docs|documentation|mkdocs|docusaurus|sphinx|markdown|uml|c4)\b"),
    ("devops", ["Cloud, DevOps & homelab", "Cloud, DevOps et homelab"],
     r"\b(kubernetes|k8s|helm|docker|compose|terraform|ansible|gitlab|github actions|ci/?cd|argo|prometheus|grafana|nginx|traefik|caddy|proxmox|homelab|self[- ]hosted|selfhosted|home ?assistant|aws|azure|gcp|serverless|cloud)\b"),
    ("security", ["Security", "Sécurité"],
     r"\b(security|pentest|ctf|owasp|vulnerab|exploit|malware|reverse|forensic|auth|oauth|jwt|crypto(graphy)?|password|secrets?)\b"),
    ("web", ["Web & frontend", "Web et frontend"],
     r"\b(react|vue|svelte|next\.?js|nuxt|astro|hugo|tailwind|css|frontend|html|javascript|typescript|web ?components|vite|webpack|node\.?js|express|fastapi|django|flask|laravel|spring)\b"),
    ("data", ["Data, finance & analytics", "Données, finance et analyse"],
     r"\b(pandas|numpy|polars|dataframe|sql|postgres|duckdb|spark|kafka|etl|analytics|backtest|trading|finance|stock|quant|time ?series|dashboard|visuali[sz]ation|plotly|matplotlib)\b"),
    ("games", ["Games, emulation & handhelds", "Jeux, émulation et consoles"],
     r"\b(game|emulat|retroarch|switch|3ds|nintendo|homebrew|rom|moonlight|steam|godot|unity|unreal|pico-?8|flash|ruffle)\b"),
    ("systems", ["Systems, Rust & embedded", "Systèmes, Rust et embarqué"],
     r"\b(rust|c\+\+|cpp|embedded|esp32|arduino|firmware|kernel|driver|linux|wasm|webassembly|compiler|llvm|zig|go(lang)?|low[- ]level|rtos|microcontroller)\b"),
    ("tools", ["Developer tools & CLI", "Outils de développement et CLI"],
     r"\b(cli|terminal|shell|zsh|bash|dotfiles|neovim|vim|vscode|editor|productivity|tool|utility|formatter|linter|testing|playwright|pytest)\b"),
    ("learning", ["Learning & references", "Apprentissage et références"],
     r"\b(awesome|tutorial|course|book|cheat ?sheet|interview|roadmap|guide|examples?|learn|curriculum|university|lecture)\b"),
]
OTHER = ("other", ["Everything else", "Tout le reste"])


def classify(repo: dict) -> list[str]:
    haystack = " ".join([
        repo.get("full_name", ""), repo.get("description") or "", " ".join(repo.get("topics") or []),
        repo.get("language") or "",
    ]).lower()
    themes = [key for key, _labels, pattern in THEMES if re.search(pattern, haystack)]
    return themes or [OTHER[0]]


def fetch(login: str) -> list[dict]:
    result = subprocess.run(
        ["gh", "api", f"users/{login}/starred?per_page=100", "--paginate", "-H", "Accept: application/vnd.github+json"],
        capture_output=True, text=True, check=True, timeout=600)
    # --paginate concatenates JSON arrays; split them safely.
    decoder = json.JSONDecoder()
    text = result.stdout.strip()
    items, pos = [], 0
    while pos < len(text):
        chunk, end = decoder.raw_decode(text, pos)
        items.extend(chunk)
        pos = end
        while pos < len(text) and text[pos] in " \n\r\t,[]":
            pos += 1
    return items


def build(items: list[dict], login: str) -> dict:
    repos = []
    for item in items:
        themes = classify(item)
        repos.append({
            "full_name": item["full_name"],
            "name": item["name"],
            "owner": item["owner"]["login"],
            "url": item["html_url"],
            "description": (item.get("description") or "").strip(),
            "language": item.get("language") or "",
            "stars": item.get("stargazers_count", 0),
            "topics": (item.get("topics") or [])[:8],
            "pushed": (item.get("pushed_at") or "")[:10],
            "archived": bool(item.get("archived")),
            "license": (item.get("license") or {}).get("spdx_id") or "",
            "homepage": item.get("homepage") or "",
            "themes": themes,
        })
    repos.sort(key=lambda r: (-r["stars"], r["full_name"].lower()))
    labels = {key: labels for key, labels, _ in THEMES}
    labels[OTHER[0]] = OTHER[1]
    counts = {}
    for repo in repos:
        counts[repo["themes"][0]] = counts.get(repo["themes"][0], 0) + 1
    themes = [{"id": key, "label": labels[key], "count": counts.get(key, 0)}
              for key in [k for k, _l, _p in THEMES] + [OTHER[0]] if counts.get(key)]
    return {"account": login, "recorded": date.today().isoformat(), "total": len(repos), "themes": themes, "repositories": repos}


FRONT = {
    "en": '---\ntitle: "Stars"\ndescription: "Repositories I starred on GitHub, grouped by theme: AI tooling, graphics, DevOps, systems and the references I keep coming back to."\ntranslationKey: stars\nlayout: stars\n---\n',
    "fr": '---\ntitle: "Étoiles"\ndescription: "Les dépôts que j’ai marqués d’une étoile sur GitHub, groupés par thème : outils IA, graphisme, DevOps, systèmes et références."\ntranslationKey: stars\nlayout: stars\n---\n',
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--login", default=LOGIN)
    parser.add_argument("--from", dest="source", help="JSON export of users/{login}/starred instead of calling gh")
    args = parser.parse_args()
    items = json.loads(Path(args.source).read_text(encoding="utf-8")) if args.source else fetch(args.login)
    data = build(items, args.login)
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CONTENT.mkdir(parents=True, exist_ok=True)
    (CONTENT / "_index.md").write_text(FRONT["en"], encoding="utf-8")
    (CONTENT / "_index.fr.md").write_text(FRONT["fr"], encoding="utf-8")
    print(f"{data['total']} starred repositories in {len(data['themes'])} themes -> {DATA.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
