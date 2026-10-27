# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = []
# ///
"""Render repository diagrams through UML-MCP and store safe local images."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from repository_docs import ROOT, load, request, save
from repository_handbooks import uml_call

OUTPUT = ROOT / "hugo/data/repository_diagram_images.json"
STATIC = ROOT / "hugo/static/repository-docs"


def image_extension(data: bytes) -> str:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "webp"
    stripped = data.lstrip()
    if stripped.startswith((b"<svg", b"<?xml")):
        lowered = stripped.lower()
        if b"<script" in lowered or b"javascript:" in lowered or b"onload=" in lowered:
            raise ValueError("Renderer returned an unsafe SVG image")
        return "svg"
    raise ValueError("Renderer did not return a supported raster image")


def render(source: str, destination: Path) -> dict:
    digest = hashlib.sha256(source.encode()).hexdigest()
    result = uml_call(
        "generate_uml",
        {
            "diagram_type": "mermaid",
            "code": source,
            "output_format": "png",
            "theme": "neutral",
        },
    )
    if not result.get("success") or not result.get("url"):
        raise ValueError("UML-MCP did not return a diagram image")
    encoded = result.get("content_base64")
    data = base64.b64decode(encoded, validate=True) if encoded else request(result["url"])
    extension = image_extension(data)
    output = destination.with_suffix("." + extension)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    return {
        "path": output.relative_to(ROOT / "hugo/static").as_posix(),
        "sha256": digest,
        "bytes": len(data),
    }


def jobs_for(note: dict, analysis: dict) -> list[tuple[str, str, Path]]:
    slug = note["slug"]
    folder = STATIC / slug
    jobs = []
    for lang in ("en", "fr"):
        source = (folder / f"architecture-{lang}.mmd").read_text(encoding="utf-8")
        jobs.append((f"overview_{lang}", source, folder / f"overview-{lang}"))
    gitdiagram = analysis.get("gitdiagram", {})
    if gitdiagram.get("status") == "available" and gitdiagram.get("mermaid"):
        system_source = gitdiagram["mermaid"].replace("flowchart TD", "flowchart LR", 1)
        system_source = system_source.replace("graph TD", "flowchart LR", 1)
        jobs.append(("system", system_source, folder / "system-overview"))
    if analysis.get("class_overview"):
        jobs.append(("types", analysis["class_overview"], folder / "code-types"))
    if analysis.get("file_overview"):
        jobs.append(("files", analysis["file_overview"], folder / "file-topology"))
    return jobs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", action="append")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    notes = load(ROOT / "hugo/data/repository_notes.json")["notes"]
    analyses = load(ROOT / "hugo/data/repository_analysis.json")["repositories"]
    selected = [note for note in notes if not args.repo or note["repo"] in args.repo]
    manifest = load(OUTPUT, {"repositories": {}})
    futures = {}
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 6))) as pool:
        for note in selected:
            current = manifest["repositories"].setdefault(note["repo"], {})
            for name, source, destination in jobs_for(note, analyses[note["repo"]]):
                digest = hashlib.sha256(source.encode()).hexdigest()
                prior = current.get(name, {})
                prior_path = ROOT / "hugo/static" / prior.get("path", "missing")
                if prior.get("sha256") == digest and prior_path.exists():
                    continue
                futures[pool.submit(render, source, destination)] = (note["repo"], name)
        errors = []
        for future in as_completed(futures):
            repo, name = futures[future]
            try:
                manifest["repositories"][repo][name] = future.result()
                print(f"{repo}: rendered {name}", flush=True)
            except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
                errors.append(f"{repo}:{name}:{type(exc).__name__}")
            save(OUTPUT, manifest)
            time.sleep(0.05)
    print(f"Rendered {len(futures) - len(errors)} diagrams; errors: {len(errors)}")
    if errors:
        print("\n".join(errors))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
