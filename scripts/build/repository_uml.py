"""Render UML diagrams for each project dossier through uml-mcp.

python scripts/build/repository_uml.py [--repo uml-mcp] [--offline]

Builds PlantUML sources from hugo/data/repository_dossiers.json (use case, component,
deployment and CI activity), renders them with the public uml-mcp REST endpoint (which
encodes them for Kroki), strips anything executable from the returned SVG and stores it
under hugo/static/repository-docs/<slug>/uml/. Files are named by a hash of their source,
so unchanged diagrams are never requested again; --offline uses those files only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
DOSSIERS = ROOT / "hugo/data/repository_dossiers.json"
NOTES = ROOT / "hugo/data/repository_notes.json"
OUT = ROOT / "hugo/data/repository_uml.json"
STATIC = ROOT / "hugo/static"
ENDPOINT = "https://uml-mcp.vercel.app/generate_diagram"
ALLOWED_HOSTS = ("https://kroki.io/",)

STYLE = """skinparam backgroundColor transparent
skinparam shadowing false
skinparam roundCorner 10
skinparam defaultFontName Arial
skinparam defaultFontSize 13
skinparam ArrowColor #4e6070
skinparam ArrowFontColor #3d4f5f
skinparam titleFontSize 14
skinparam actorBorderColor #006a62
skinparam actorBackgroundColor #e9f3f4
skinparam usecaseBorderColor #006a62
skinparam usecaseBackgroundColor #e9f3f4
skinparam componentBorderColor #006a62
skinparam componentBackgroundColor #e9f3f4
skinparam interfaceBorderColor #006a62
skinparam interfaceBackgroundColor #ffffff
skinparam nodeBorderColor #4e6070
skinparam nodeBackgroundColor #f4f8fb
skinparam databaseBorderColor #006a62
skinparam databaseBackgroundColor #ffffff
skinparam cloudBorderColor #4e6070
skinparam cloudBackgroundColor #f0f5fa
skinparam artifactBorderColor #006a62
skinparam artifactBackgroundColor #ffffff
skinparam rectangleBorderColor #b0c2d3
skinparam activityBorderColor #006a62
skinparam activityBackgroundColor #e9f3f4
skinparam partitionBorderColor #b0c2d3
skinparam stereotypeCBackgroundColor #ffffff"""


def q(text, limit=40):
    """Text that is safe inside a quoted PlantUML label."""
    text = re.sub(r"[\"\\{}<>|;]", "'", str(text)).replace("\n", " ").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def wrap(body, kind):
    return f"@startuml\n{STYLE}\n{body.strip()}\n@enduml\n"


def callers(public, fr):
    actors = []
    if public["routes"]:
        actors.append(("http", "Client HTTP" if fr else "HTTP client"))
    if public["mcp"]:
        actors.append(("mcp", "Client MCP" if fr else "MCP client"))
    if public["cli"] or any(e["kind"] == "console script" for e in public["entry_points"]):
        actors.append(("cli", "Utilisateur CLI" if fr else "CLI user"))
    return actors


def usecase_uml(repo, d, fr):
    public = d["public"]
    actors = callers(public, fr)
    if not actors:
        return None
    lines = ["left to right direction"]
    lines += [f'actor "{label}" as A_{key}' for key, label in actors]
    cases = []
    groups = {}
    for route in public["routes"]:
        segment = route["path"].strip("/").split("/")[0] or ""
        groups.setdefault(segment, []).append(route)
    for segment, items in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:6]:
        methods = "/".join(sorted({r["method"] for r in items}))[:20]
        label = f"{methods} /{segment}" + (f" ({len(items)} routes)" if len(items) > 1 else "")
        cases.append(("http", label))
    for tool in public["mcp"][:6]:
        verb = {"tool": "Outil" if fr else "Tool", "resource": "Ressource" if fr else "Resource", "prompt": "Prompt"}.get(tool["kind"], tool["kind"])
        cases.append(("mcp", f"{verb} {tool['name']}"))
    commands = [c for c in public["cli"] if c["kind"] in {"command", "subcommand"}][:5]
    if commands:
        cases += [("cli", f"{'Commande' if fr else 'Command'} {c['name']}") for c in commands]
    elif public["cli"]:
        n = public["cli_total"]
        cases.append(("cli", f"Lancer l'outil ({n} options)" if fr else f"Run the tool ({n} options)"))
    elif any(e["kind"] == "console script" for e in public["entry_points"]):
        names = [e["name"] for e in public["entry_points"] if e["kind"] == "console script"][:3]
        cases.append(("cli", ("Lancer " if fr else "Run ") + ", ".join(names)))
    if len(cases) < 2:
        return None
    lines.append(f'rectangle "{q(repo)}" {{')
    lines += [f'  usecase "{q(label, 44)}" as U{i}' for i, (_, label) in enumerate(cases)]
    lines.append("}")
    lines += [f"A_{key} --> U{i}" for i, (key, _) in enumerate(cases)]
    return "\n".join(lines)


def component_uml(repo, d, fr):
    i = 1 if fr else 0
    inner = []
    if d.get("flow") and d["flow"].get("groups"):
        inner = [g["label"] for g in d["flow"]["groups"]][:6]
    else:
        inner = [m["name"] for m in d["modules"]["items"] if m["name"] != "(root)"][:5]
    provided = [label for _, label in callers(d["public"], fr)]
    required = [s["label"][i] for s in d["integrations"]["services"][:6]]
    stores = [e["label"][i] for e in d["database"]["engines"][:3]]
    if len(provided) + len(required) + len(stores) < 2 or not inner:
        return None
    lines = ["left to right direction"]
    lines += [f'interface "{q(p, 24)}" as P{n}' for n, p in enumerate(provided)]
    lines.append(f'component "{q(repo)}" as SYS {{')
    lines += [f'  component "{q(c, 30)}" as C{n}' for n, c in enumerate(inner)]
    lines.append("}")
    lines += [f"P{n} - SYS" for n in range(len(provided))]
    lines += [f'component "{q(r, 30)}" as R{n} <<external>>' for n, r in enumerate(required)]
    lines += [f'database "{q(s, 30)}" as S{n}' for n, s in enumerate(stores)]
    uses = "utilise" if fr else "uses"
    lines += [f"SYS ..> R{n} : {uses}" for n in range(len(required))]
    lines += [f"SYS ..> S{n}" for n in range(len(stores))]
    return "\n".join(lines)


PLATFORMS = {
    "Vercel": "cloud", "Netlify": "cloud", "Fly.io": "cloud", "Render": "cloud",
    "Cloudflare Workers": "cloud", "Kubernetes manifests": "node",
    "PlatformIO firmware build": "node", "Docker image": "node", "Docker Compose stack": "node",
}


def deployment_uml(repo, d, fr):
    i = 1 if fr else 0
    svc = d["services"]
    hosting = [h for h in svc["hosting"] if h["label"][0] in PLATFORMS]
    containers = svc.get("containers") or []
    images = svc.get("base_images") or []
    if not (hosting or containers or images):
        return None
    lines = []
    if containers:
        lines.append('node "Docker Compose" as H {')
        lines += [f'  node "{q(c, 28)}" as N{n} <<container>>' for n, c in enumerate(containers[:10])]
        lines.append("}")
        app = "N0"
    else:
        host = hosting[0] if hosting else None
        shape = PLATFORMS.get(host["label"][0], "node") if host else "node"
        title = host["label"][i] if host else ("Conteneur" if fr else "Container")
        lines.append(f'{shape} "{q(title, 30)}" as H {{')
        lines.append(f'  artifact "{q(repo)}" as APP')
        lines.append("}")
        app = "APP"
    for n, image in enumerate(images[:3]):
        lines.append(f'artifact "FROM {q(image["image"], 34)}" as IMG{n}')
        lines.append(f"IMG{n} ..> {app} : {'construit' if fr else 'builds'}")
    for n, other in enumerate(h for h in hosting[1:4] if PLATFORMS[h["label"][0]] == "cloud"):
        lines.append(f'cloud "{q(other["label"][i], 30)}" as X{n}')
        lines.append(f"X{n} ..> {app}")
    for n, engine in enumerate(d["database"]["engines"][:3]):
        if engine["kind"] in {"sql", "document", "key-value", "orm"}:
            lines.append(f'database "{q(engine["label"][i], 30)}" as DB{n}')
            lines.append(f"{app} --> DB{n}")
    for n, ext in enumerate(d["integrations"]["services"][:4]):
        lines.append(f'cloud "{q(ext["label"][i], 30)}" as E{n}')
        lines.append(f"{app} ..> E{n}")
    return "\n".join(lines)


def activity_uml(repo, d, fr):
    workflows = [w for w in d["tests"]["workflows"] if any(j["steps"] for j in w.get("jobs", []))]
    if not workflows:
        return None
    flow = workflows[0]
    jobs = [j for j in flow["jobs"] if j["steps"]][:5]
    roots = [j for j in jobs if not j["needs"]]
    rest = [j for j in jobs if j["needs"]]

    def partition(job, indent=""):
        out = [f'{indent}partition "{q(job.get("title") or job["name"], 30)}" {{']
        out += [f"{indent}  :{q(step, 44).replace(':', ' ')};" for step in job["steps"][:8]]
        out.append(f"{indent}}}")
        return out

    lines = [f'title {q(flow["name"], 50)}', "start"]
    if len(roots) > 1:
        for n, job in enumerate(roots):
            lines.append("fork" if n == 0 else "fork again")
            lines += partition(job, "  ")
        lines.append("end fork")
    else:
        for job in roots:
            lines += partition(job)
    for job in rest:
        lines += partition(job)
    lines.append("stop")
    return "\n".join(lines)


DIAGRAMS = [
    ("usecase", "usecase", usecase_uml,
     ["Use cases", "Cas d’utilisation"],
     ["Each actor is a kind of caller, linked to what it can ask the project to do.", "Chaque acteur est un type d’appelant, relié à ce qu’il peut demander au projet."]),
    ("component", "component", component_uml,
     ["Components and interfaces", "Composants et interfaces"],
     ["The project offers the interfaces drawn as circles and depends on the external components and databases its dashed arrows reach.", "Le projet offre les interfaces dessinées en cercle et dépend des composants externes et bases de données que ses flèches pointillées atteignent."]),
    ("deployment", "deployment", deployment_uml,
     ["Deployment", "Déploiement"],
     ["The outer node is where the code runs. Each base image points to what it builds, solid arrows lead to databases and dashed ones to outside services.", "Le nœud extérieur est l’endroit où le code s’exécute. Chaque image de base pointe vers ce qu’elle construit, les flèches pleines mènent aux bases de données et les pointillées aux services externes."]),
    ("activity", "activity", activity_uml,
     ["CI pipeline", "Pipeline CI"],
     ["The main GitHub Actions workflow runs these steps. Jobs that run in parallel sit side by side.", "Le workflow GitHub Actions principal suit ces étapes. Les tâches lancées en parallèle sont côte à côte."]),
]


def sanitize(svg):
    """Keep drawing markup only: no scripts, event handlers, foreign HTML or embedded source."""
    svg = re.sub(r"<\?plantuml[^>]*\?>", "", svg)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.DOTALL)
    svg = re.sub(r"<script\b.*?</script>", "", svg, flags=re.DOTALL | re.IGNORECASE)
    svg = re.sub(r"<foreignObject\b.*?</foreignObject>", "", svg, flags=re.DOTALL | re.IGNORECASE)
    svg = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", svg, flags=re.IGNORECASE)
    svg = re.sub(r"(href\s*=\s*[\"'])\s*javascript:[^\"']*", r"\1#", svg, flags=re.IGNORECASE)
    if not svg.lstrip().startswith(("<svg", "<?xml")) or "<svg" not in svg:
        raise ValueError("Renderer did not return SVG")
    return svg


def fetch(url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"User-Agent": "CV-repository-uml/1.0"}
    if data:
        headers["Content-Type"] = "application/json"
    with urlopen(Request(url, data=data, headers=headers), timeout=60) as response:
        body = response.read(3_000_001)
    if len(body) > 3_000_000:
        raise ValueError("Diagram exceeds the size limit")
    return body


def render(code, kind):
    answer = json.loads(fetch(ENDPOINT, {"lang": "plantuml", "type": kind, "code": code, "output_format": "svg"}))
    url = answer.get("url") or ""
    if not url.startswith(ALLOWED_HOSTS):
        raise ValueError("Unexpected renderer URL")
    return sanitize(fetch(url).decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", action="append", help="Repository name; repeat to select several")
    parser.add_argument("--offline", action="store_true", help="Use stored SVG files only")
    args = parser.parse_args()
    dossiers = json.loads(DOSSIERS.read_text(encoding="utf-8"))["repositories"]
    slugs = {n["repo"]: n["slug"] for n in json.loads(NOTES.read_text(encoding="utf-8"))["notes"]}
    output = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"schema_version": 1, "repositories": {}}
    failures = 0
    for repo, d in dossiers.items():
        if args.repo and repo not in args.repo:
            continue
        slug = slugs[repo]
        folder = STATIC / "repository-docs" / slug / "uml"
        entries, keep = [], set()
        for key, kind, build, title, note in DIAGRAMS:
            sources = [build(repo, d, False), build(repo, d, True)]
            if not all(sources):
                continue
            item = {"key": key, "title": title, "note": note, "svg": [], "source": []}
            for body in sources:
                code = wrap(body, kind)
                name = hashlib.sha256(code.encode()).hexdigest()[:16] + ".svg"
                target = folder / name
                keep.add(name)
                if not target.exists():
                    if args.offline:
                        item = None
                        break
                    try:
                        svg = render(code, kind)
                    except (OSError, ValueError, KeyError) as exc:
                        print(f"{repo} {key}: render failed ({type(exc).__name__})", flush=True)
                        failures += 1
                        item = None
                        break
                    folder.mkdir(parents=True, exist_ok=True)
                    target.write_text(svg, encoding="utf-8")
                    time.sleep(0.4)  # stay well under the endpoint's rate limit
                item["svg"].append(f"repository-docs/{slug}/uml/{name}")
                item["source"].append(code)
            if item:
                entries.append(item)
        # Remove SVGs from earlier sources that no diagram uses any more.
        if folder.exists():
            for old in folder.glob("*.svg"):
                if old.name not in keep and re.fullmatch(r"[0-9a-f]{16}\.svg", old.name):
                    old.unlink()
        output["repositories"][repo] = entries
        print(f"{repo}: {', '.join(e['key'] for e in entries) or 'no UML diagrams'}", flush=True)
    output["repositories"] = dict(sorted(output["repositories"].items(), key=lambda kv: kv[0].lower()))
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
