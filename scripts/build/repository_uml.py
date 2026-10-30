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
    # C4-PlantUML brings its own styling; the skin parameters are for plain UML diagrams.
    style = "" if kind == "c4plantuml" else STYLE + "\n"
    return f"@startuml\n{style}{body.strip()}\n@enduml\n"


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


EXT_LANG = {".py": "Python", ".ts": "TypeScript", ".tsx": "React", ".jsx": "React", ".vue": "Vue", ".js": "JavaScript",
            ".rs": "Rust", ".cs": "C#", ".java": "Java", ".kt": "Kotlin", ".php": "PHP", ".rb": "Ruby", ".go": "Go",
            ".cpp": "C++", ".hpp": "C++", ".cc": "C++", ".h": "C/C++", ".c": "C", ".html": "HTML", ".swift": "Swift",
            ".blade.php": "Blade", ".ino": "Arduino"}


def layer_tech(d, keys):
    """Main language of the modules in the given layers, from their file extensions."""
    counts = {}
    for layer in d["layers"]:
        if layer["key"] in keys:
            for module in layer["modules"]:
                for ext in module["extensions"][:1]:
                    if ext in EXT_LANG:
                        counts[EXT_LANG[ext]] = counts.get(EXT_LANG[ext], 0) + module["files"]
    return max(counts, key=counts.get) if counts else ""


def c4_people_and_systems(d, fr):
    i = 1 if fr else 0
    people = callers(d["public"], fr)
    # Transports (WebSocket, Wi-Fi client, console network stack) are how systems talk, not systems.
    externals = [s["label"][i] for s in d["integrations"]["services"] if s.get("kind") != "transport"][:6]
    stores = [e["label"][i] for e in d["database"]["engines"] if e["kind"] in {"sql", "document", "key-value", "orm"}][:3]
    return people, externals, stores


def c4_context_uml(repo, d, fr):
    """C4 level 1: the people who use the project and the outside systems it depends on."""
    people, externals, stores = c4_people_and_systems(d, fr)
    if not (people or externals or stores or d.get("files_scanned")):
        return None
    intro = q((d.get("_intro") or ["", ""])[1 if fr else 0].split(". ")[0], 70)
    lines = ["!include <C4/C4_Context>", "LAYOUT_LEFT_RIGHT()"]
    lines += [f'Person(P_{key}, "{label}")' for key, label in people]
    lines.append(f'System(SYS, "{q(repo)}", "{intro}")')
    lines += [f'System_Ext(E{n}, "{q(e, 30)}")' for n, e in enumerate(externals)]
    lines += [f'SystemDb(D{n}, "{q(s, 30)}")' for n, s in enumerate(stores)]
    use = "Utilise" if fr else "Uses"
    lines += [f'Rel(P_{key}, SYS, "{use}")' for key, _ in people]
    lines += [f'Rel(SYS, E{n}, "{"Appelle" if fr else "Calls"}")' for n in range(len(externals))]
    lines += [f'Rel(SYS, D{n}, "{"Lit et écrit" if fr else "Reads and writes"}")' for n in range(len(stores))]
    return "\n".join(lines)


def c4_container_uml(repo, d, fr):
    """C4 level 2: deployable parts inside the project boundary and how they connect."""
    people, externals, stores = c4_people_and_systems(d, fr)
    present = {layer["key"] for layer in d["layers"]}
    containers = []  # (id, label, technology, kind)
    compose = d["services"].get("containers") or []
    if compose:
        def service_key(value):
            return re.sub(r'[^a-z0-9]', '', value.lower().removesuffix(' server'))
        internal = {service_key(name) for name in compose}
        externals = [name for name in externals if service_key(name) not in internal]
    if compose:
        containers = [(f"C{n}", name, "Docker", "container") for n, name in enumerate(compose[:8])]
    else:
        # A source layer is not a deployable container. Only known entry points
        # or hosting evidence support a single application boundary here.
        if not (callers(d["public"], fr) or d["public"].get("entry_points") or d["services"].get("hosting")):
            return None
        containers.append(("APP", repo, layer_tech(d, present), "container"))
    for n, store in enumerate(stores):
        containers.append((f"DB{n}", store, "", "db"))
    if not containers:
        return None
    lines = ["!include <C4/C4_Container>", "LAYOUT_LEFT_RIGHT()"]
    lines += [f'Person(P_{key}, "{label}")' for key, label in people]
    lines.append(f'System_Boundary(SYS, "{q(repo)}") {{')
    for cid, label, tech, kind in containers:
        macro = "ContainerDb" if kind == "db" else "Container"
        lines.append(f'  {macro}({cid}, "{q(label, 30)}", "{q(tech, 20)}")')
    lines.append("}")
    lines += [f'System_Ext(E{n}, "{q(e, 30)}")' for n, e in enumerate(externals)]
    ids = [c[0] for c in containers if c[3] == "container"]
    use, call, rw = ("Utilise", "Appelle", "Lit et écrit") if fr else ("Uses", "Calls", "Reads and writes")
    if compose:
        # The service named after the project is the one people call and that calls out;
        # the other Compose services are its companions, so no chain is invented between them.
        own = next((c[0] for c in containers if c[3] == "container" and re.sub(r"\W", "", c[1].lower()) in re.sub(r"\W", "", repo.lower())), None)
        entry = last = own or (ids[0] if ids else containers[0][0])
    else:
        entry = ids[0] if ids else containers[0][0]
        last = ids[-1] if ids else entry
    lines += [f'Rel(P_{key}, {entry}, "{use}")' for key, _ in people]
    lines += [f'Rel({last}, {cid}, "{rw}")' for cid, _, _, kind in containers if kind == "db"]
    lines += [f'Rel({last}, E{n}, "{call}")' for n in range(len(externals))]
    return "\n".join(lines)


def c4_component_uml(repo, d, fr):
    """Source modules grouped by classified layer, without inferred call edges."""
    layers = [layer for layer in d.get("layers", []) if layer.get("modules")]
    if not layers:
        return None
    i = int(fr)
    lines = ['!include <C4/C4_Component>', 'LAYOUT_TOP_DOWN()',
             f'System_Boundary(SYS, "{q(repo)}") {{']
    for n, layer in enumerate(layers):
        label = layer.get("label", [layer["key"]] * 2)[i]
        lines.append(f'Boundary(L{n}, "{q(label)}", "layer") {{')
        for m, module in enumerate(layer["modules"]):
            tech = ", ".join(dict.fromkeys(EXT_LANG.get(e, e) for e in module.get("extensions", [])))
            count = module.get("files", 0)
            lines.append(f'Component(M{n}_{m}, "{q(module.get("name", layer["key"]), 60)}", "{q(tech)}", "{count} {"fichiers" if fr else "files"}")')
        if layer.get("more_modules"):
            lines.append(f'Component(M{n}_more, "+{layer["more_modules"]} modules", "", "")')
        lines.append('}')
    lines.append('}')
    return '\n'.join(lines)


def c4_code_uml(repo, d, fr):
    """C4 level 4 uses UML declarations grouped by actual source file."""
    items = []
    seen = set()
    for item in d.get("logic", {}).get("types", []) + d.get("entities", {}).get("items", []):
        key = (item.get("file"), item.get("name"))
        if all(key) and key not in seen:
            seen.add(key)
            items.append(item)
    functions = [item for item in d.get("logic", {}).get("files", []) if item.get("functions")]
    if not items and not functions:
        return None
    files = {}
    for item in items:
        files.setdefault(item["file"], []).append(item)
    lines = ['top to bottom direction', 'hide empty members', f'package "{q(repo)}" {{']
    for n, (path, declarations) in enumerate(files.items()):
        lines.append(f'package "{q(path, 90)}" as F{n} {{')
        for m, item in enumerate(declarations):
            lines.append(f'class "{q(item["name"], 60)}" as T{n}_{m} {{')
            for field in item.get("fields", []):
                lines.append('  ' + q(field, 65))
            for method in item.get("methods", []):
                lines.append('  ' + q(method, 65) + '()')
            lines.append('}')
        lines.append('}')
    for n, item in enumerate(functions):
        lines.append(f'object "{q(item["file"], 90)}" as FN{n} {{')
        for function in item["functions"]:
            lines.append('  ' + q(function, 65) + '()')
        lines.append('}')
    lines.append('}')
    return '\n'.join(lines)


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
    ("c4context", "c4plantuml", c4_context_uml,
     ["1 · System context", "1 · Contexte du système"],
     ["The widest C4 view: who uses the project and which outside systems and data stores it relies on.", "La vue C4 la plus large : qui utilise le projet et sur quels systèmes et stockages externes il s’appuie."]),
    ("c4container", "c4plantuml", c4_container_uml,
     ["2 · Containers", "2 · Conteneurs"],
     ["One level closer: the parts that run separately inside the project, their main language and how calls flow between them.", "Un niveau plus près : les parties qui s’exécutent séparément dans le projet, leur langage principal et le chemin des appels entre elles."]),
    ("c4component", "c4plantuml", c4_component_uml,
     ["3 · Components and layers", "3 · Composants et couches"],
     ["Modules grouped by source-layer classification. Boundaries show organization, not runtime isolation or call relationships.", "Modules regroupés par couche du code. Les limites indiquent l’organisation, sans affirmer une isolation à l’exécution ni des appels."]),
    ("c4code", "class", c4_code_uml,
     ["4 · Code", "4 · Code"],
     ["Selected declarations, fields and methods grouped by source file. No inheritance or call edges are inferred.", "Déclarations, champs et méthodes sélectionnés, regroupés par fichier source. Aucun héritage ni appel n’est déduit."]),
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
    notes = json.loads(NOTES.read_text(encoding="utf-8"))["notes"]
    slugs = {n["repo"]: n["slug"] for n in notes}
    intros = {n["repo"]: n["intro"] for n in notes}
    output = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"schema_version": 1, "repositories": {}}
    failures = 0
    for repo, d in dossiers.items():
        if args.repo and repo not in args.repo:
            continue
        slug = slugs[repo]
        folder = STATIC / "repository-docs" / slug / "uml"
        entries, keep = [], set()
        for key, kind, build, title, note in DIAGRAMS:
            context = dict(d, _intro=intros.get(repo))  # the C4 context box describes the system
            sources = [build(repo, context, False), build(repo, context, True)]
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
