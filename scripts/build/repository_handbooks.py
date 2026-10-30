# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = []
# ///
"""Build reader-facing guides from pinned public repository evidence.

Run after repository_docs.py. --render calls the user-selected UML-MCP service;
ordinary/offline builds use recorded results and never contact a diagram service.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import PurePosixPath
from urllib.parse import quote, urlsplit

from repository_docs import CACHE, ROOT, fetch_blob, load, request, save

OUTPUT = ROOT / "hugo/data/repository_handbooks.json"
CATEGORIES = {
    "setup": (
        "Prerequisites and first run",
        "Prérequis et premier essai",
        r"prerequis|requirement|install|quick.?start|getting started|build from|local development|démarrage",
    ),
    "configuration": (
        "Configuration and usage",
        "Configuration et utilisation",
        r"config|environment|usage|utilisation|parameter|variable|CLI|setup",
    ),
    "api": (
        "API and integration",
        "API et intégration",
        r"\bAPI\b|endpoint|authentic|pagination|rate limit|SDK|MCP tools|tool reference",
    ),
    "operations": (
        "Operations and troubleshooting",
        "Exploitation et dépannage",
        r"troubleshoot|debug|deploy|rollback|updat|uninstall|monitor|dépannage",
    ),
    "contributing": (
        "Development and contributions",
        "Développement et contributions",
        r"contribut|test|develop|onboard",
    ),
}
KINDS = {
    "configuration": [
        ".dotfiles",
        "another-install-script",
        "MediaBoxDockerCompose",
        "architecture",
        "antoinebou12",
        "uml-skill",
    ],
    "hardware": [
        "Artemis-Switch",
        "Artemis-N3DS",
        "sm64coopdx-switch-N3DS",
        "nxsand",
        "switch-wifi",
        "NX-Activity-Log",
        "ESP32-7SEG",
        "HDR-10bpp-Display-Test",
        "Pan-Tilt-Controller",
    ],
    "library": [
        "Dimension",
        "Serilog.Sinks.SentrySDK",
        "marketwatch",
        "nova-backtest",
        "ipc-toolkit",
        "jsonresume-theme-kendall",
    ],
    "integration": ["ComfyUI-UML", "bloc", "hass_renpho", "GithubSimpleFileDownloader"],
    "service": [
        "uml-mcp",
        "donneesqc-mcp",
        "D2COpenAIPlugin",
        "ChitUI",
        "kroki-playground",
        "DasherControl",
        "Maestro",
        "SpringBootFilesUploader",
        "novatorem",
        "AuthLaravel",
        "linkshare",
        "TCH099",
        "WordsEnigma",
    ],
    "application": [
        "AudioTranscript",
        "CV",
        "RawAnalyser",
        "FlashGames",
        "GreenScreenVideotoAlphaPNGs",
        "retroarch-web-games",
        "hydra",
        "LLM2SVG",
    ],
}
LABELS = {
    "configuration": [
        "Configuration and automation",
        "Configuration et automatisation",
    ],
    "hardware": ["Hardware and graphics", "Matériel et infographie"],
    "library": ["Library", "Bibliothèque"],
    "integration": ["Integration", "Intégration"],
    "service": ["Application and services", "Application et services"],
    "application": ["Application and tools", "Application et outils"],
}


def public_url(value):
    """Only publish ordinary credential-free HTTPS links from known evidence."""
    try:
        parsed = urlsplit(value or "")
        return bool(
            parsed.scheme == "https"
            and parsed.hostname
            and not parsed.username
            and not parsed.password
            and not parsed.query
            and parsed.hostname not in {"localhost", "127.0.0.1", "example.com"}
        )
    except ValueError:
        return False


def sections(text):
    """Parse ATX sections without treating headings in fenced examples as sections."""
    result, current, fence = [], None, None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker[1][0]
            fence = None if fence == token else token if fence is None else fence
        heading = re.match(r"^#{1,6}\s+(.+?)\s*#*$", line) if fence is None else None
        if heading:
            current = {"heading": heading[1], "line": number, "lines": []}
            result.append(current)
        elif current:
            current["lines"].append(line)
    return result


def excerpt(lines):
    """Plain prose only; commands remain in the separately sourced install panel."""
    text = "\n".join(lines)
    text = re.sub(r"(`{3,}|~{3,})[^\n]*\n[\s\S]*?(?:\1|$)", "", text)
    text = re.sub(r"<!--[\s\S]*?-->", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    safe = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
        # A bare "#" renders as an empty heading once the excerpt goes through Markdown.
        and not re.fullmatch(r"#+", line.strip())
        and not re.search(
            r"https?://|token\s*[=:]|password\s*[=:]|secret\s*[=:]|yourusername",
            line,
            re.IGNORECASE,
        )
    ]
    text = "\n".join(safe).replace("**", "").replace("`", "")
    return text[:900].rsplit(" ", 1)[0] + "…" if len(text) > 900 else text


def unique_title(title, path, seen):
    """Return the heading, or "heading (FILE.md)" when an earlier document already used it."""
    for candidate in (title, f"{title} ({PurePosixPath(path).name})", f"{title} ({path})"):
        if candidate.lower() not in seen:
            seen.add(candidate.lower())
            return candidate
    return f"{title} ({path})"


def doc_candidate(entry):
    path = PurePosixPath(entry["path"])
    excluded = {
        "node_modules",
        "vendor",
        "third_party",
        "external",
        "target",
        "dist",
        "archive",
        "public",
        "_site",
        ".git",
    }
    return (
        entry.get("type") == "blob"
        and entry.get("mode") != "120000"
        and entry.get("size", 0) < 200_000
        and not path.is_absolute()
        and not any(part in excluded or part == ".." for part in path.parts)
        and path.suffix.lower() in {".md", ".rst"}
        and bool(
            re.search(
                r"readme|install|contribut|deploy|troubleshoot|getting.started|api.reference|configuration|quickstart|runbook",
                path.name,
                re.IGNORECASE,
            )
        )
    )


def diagram_source(note, locale):
    lines = ["flowchart TD"]
    for index, pair in enumerate(note["nodes"]):
        label = (
            pair[locale]
            .replace('"', "#quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        lines.append(f'  n{index}["{label}"]')
    lines += [f"  n{a} --> n{b}" for a, b in note["edges"]]
    return "\n".join(lines) + "\n"


def uml_call(name, arguments):
    raw = request(
        "https://uml-mcp.vercel.app/mcp",
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
    ).decode()
    records = [
        json.loads(line[6:]) for line in raw.splitlines() if line.startswith("data: ")
    ]
    answer = records[-1] if records else json.loads(raw)
    result = answer.get("result", {})
    if answer.get("error") or result.get("isError"):
        raise ValueError("UML-MCP rejected the diagram request")
    if result.get("structuredContent"):
        return result["structuredContent"]
    for block in result.get("content", []):
        if block.get("type") == "text":
            try:
                value = json.loads(block["text"])
                if isinstance(value, dict):
                    return value
            except json.JSONDecodeError:
                continue
    raise ValueError("UML-MCP returned no structured diagram result")


def build(note, offline):
    inputs = load(CACHE / note["slug"] / "inputs.json")
    if inputs["metadata"]["private"]:
        raise ValueError("Only public repositories can be documented")
    commit = inputs["commit"]
    base = f"{note['url']}/blob/{commit}/"
    candidates = sorted(
        filter(doc_candidate, inputs["tree"]["tree"]),
        key=lambda e: (len(PurePosixPath(e["path"]).parts), len(e["path"]), e["path"]),
    )
    chapters = {key: [] for key in CATEGORIES}
    documents, failures = [], []
    # The same paragraph often sits in README and CONTRIBUTING or docs/; keep its first copy only.
    seen_text = set()
    # Different documents reuse headings ("Contributing", "Installation"); later ones name their file.
    seen_titles = set()
    for entry in candidates[:24]:
        try:
            text = fetch_blob(note["repo"], commit, entry, offline)
        except (OSError, ValueError) as exc:
            failures.append({"path": entry["path"], "error": type(exc).__name__})
            continue
        documents.append(
            {
                "path": entry["path"],
                "url": base + quote(entry["path"]),
                "sha": entry["sha"],
            }
        )
        for section in sections(text):
            for key, (_, _, pattern) in CATEGORIES.items():
                if (
                    re.search(pattern, section["heading"], re.IGNORECASE)
                    and len(chapters[key]) < 5
                ):
                    preview = excerpt(section["lines"])
                    normalized = re.sub(r"\W+", " ", preview).strip().lower()
                    if preview and re.search(r"\w", preview) and normalized not in seen_text:
                        seen_text.add(normalized)
                        chapters[key].append(
                            {
                                # Headings are shown as plain text, so drop inline Markdown markers.
                                "title": unique_title(re.sub(r"\*\*|__|`", "", section["heading"]).strip(), entry["path"], seen_titles),
                                "text": preview,
                                "url": base
                                + quote(entry["path"])
                                + f"#L{section['line']}",
                                "file": entry["path"],
                            }
                        )
                    break
    metadata = inputs["metadata"]
    kind = next(key for key, names in KINDS.items() if note["repo"] in names)
    licence = metadata.get("license") or {}
    links = [
        {
            "label": ["Repository README", "README du dépôt"],
            "url": note["url"] + "#readme",
        }
    ]
    if public_url(metadata.get("homepage")):
        links.append(
            {
                "label": [
                    "Repository website"
                    if not note["fork"]
                    else "Website listed by this fork",
                    "Site du dépôt" if not note["fork"] else "Site indiqué par ce fork",
                ],
                "url": metadata["homepage"],
            }
        )
    if metadata.get("has_issues"):
        links.append(
            {
                "label": ["Issues and questions", "Problèmes et questions"],
                "url": note["url"] + "/issues",
            }
        )
    parent = metadata.get("parent", {})
    if note["fork"] and public_url(parent.get("html_url")):
        links.append(
            {
                "label": ["Upstream project", "Projet d’origine"],
                "url": parent["html_url"],
            }
        )
    return {
        "repo": note["repo"],
        "slug": note["slug"],
        "commit": commit,
        "kind": kind,
        "kind_label": LABELS[kind],
        "links": links,
        "license": licence.get("spdx_id")
        if licence.get("spdx_id") != "NOASSERTION"
        else None,
        "stars": metadata.get("stargazers_count", 0),
        "recorded": inputs["fetched_at"][:10],
        "chapters": [
            {"id": key, "title": list(CATEGORIES[key][:2]), "entries": entries}
            for key, entries in chapters.items()
            if entries
        ],
        "documents": documents,
        "coverage": {
            "selected": min(24, len(candidates)),
            "available": len(candidates),
            "failures": failures,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--repo", action="append")
    args = parser.parse_args()
    if args.offline and args.render:
        parser.error("--render requires network access")
    notes = load(ROOT / "hugo/data/repository_notes.json")["notes"]
    if args.repo and set(args.repo) - {n["repo"] for n in notes}:
        parser.error("Repository is not in the public inventory")
    data = load(OUTPUT, {"repositories": {}})
    errors = []
    for note in notes:
        if args.repo and note["repo"] not in args.repo:
            continue
        guide = build(note, args.offline)
        previous = data["repositories"].get(note["repo"], {})
        guide["diagrams"] = {}
        for locale, lang in enumerate(("en", "fr")):
            code = diagram_source(note, locale)
            digest = hashlib.sha256(code.encode()).hexdigest()
            prior = previous.get("diagrams", {}).get(lang, {})
            destination = (
                ROOT
                / "hugo/static/repository-docs"
                / note["slug"]
                / f"architecture-{lang}.mmd"
            )
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(code, encoding="utf-8")
            result = prior if prior.get("sha256") == digest else {}
            if args.render and not result.get("success"):
                try:
                    rendered = uml_call(
                        "generate_uml",
                        {
                            "diagram_type": "mermaid",
                            "code": code,
                            "output_format": "svg",
                            "theme": "neutral",
                        },
                    )
                    result = {
                        key: rendered.get(key)
                        for key in ("success", "url", "playground", "error")
                    }
                    result["checked"] = datetime.now(UTC).isoformat()
                    if not result.get("success"):
                        errors.append(note["repo"] + ":" + lang)
                except (OSError, ValueError) as exc:
                    result = {"success": False, "error": type(exc).__name__}
                    errors.append(note["repo"] + ":" + lang)
            result["sha256"] = digest
            guide["diagrams"][lang] = result
        data["repositories"][note["repo"]] = guide
        save(OUTPUT, data)
        print(
            f"{note['repo']}: {len(guide['documents'])} source documents, {len(guide['chapters'])} guide sections",
            flush=True,
        )
    print(f"Diagram errors: {len(errors)}", flush=True)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
