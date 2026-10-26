# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["tree-sitter-language-pack==0.13.0", "tree-sitter==0.25.2"]
# ///
"""Refresh public-repository documentation without executing repository code.

uv run --python 3.13 scripts/build/repository_docs.py [--repo uml-mcp] [--offline]
Raw inputs stay in ignored _site; only derived documentation is published.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "_site/repository-docs-cache"
DATA = ROOT / "hugo/data/repository_analysis.json"
EXPORT = ROOT / "hugo/static/repository-docs"
OWNER = "antoinebou12"
MAX_BYTES = 4_000_000
LANGUAGES = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".rs": "rust",
    ".c": "c",
    ".h": "cpp",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".cc": "cpp",
    ".hh": "cpp",
    ".cs": "csharp",
    ".java": "java",
    ".kt": "kotlin",
    ".php": "php",
    ".rb": "ruby",
    ".go": "go",
    ".swift": "swift",
    ".sh": "bash",
    ".bash": "bash",
    ".lua": "lua",
}
EXCLUDED = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "vendor",
    "third_party",
    "third-party",
    "extern",
    "external",
    "submodules",
    "build",
    "dist",
    "out",
    "target",
    "coverage",
    "archive",
    "archives",
    "docs",
    "_site",
    "public",
    "generated",
    "__pycache__",
}
MANIFESTS = {
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "requirements.txt",
    "CMakeLists.txt",
    "Makefile",
    "build.gradle.kts",
    "composer.json",
    "Gemfile",
    "platformio.ini",
    "docker-compose.yml",
    "compose.yml",
}
DECLARATIONS = {
    "class_definition": "class",
    "class_declaration": "class",
    "abstract_class_declaration": "class",
    "class_specifier": "class",
    "struct_specifier": "struct",
    "struct_declaration": "struct",
    "struct_item": "struct",
    "trait_item": "trait",
    "enum_item": "enum",
    "interface_declaration": "interface",
    "record_declaration": "record",
    "trait_declaration": "trait",
    "class": "class",
}
METHODS = {
    "function_definition",
    "function_item",
    "method_definition",
    "method_declaration",
    "method_signature",
    "abstract_method_signature",
    "constructor_declaration",
    "function_declaration",
    "method",
    "singleton_method",
}
NET = threading.Semaphore(8)
MCP_LOCK = threading.Lock()
MCP_LAST = 0.0


def load(path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def github(endpoint):
    result = subprocess.run(
        ["gh", "api", endpoint],
        capture_output=True,
        check=True,
        encoding="utf-8",
        timeout=60,
    )
    return json.loads(result.stdout)


def request(url, payload=None):
    headers = {"User-Agent": "CV-repository-documentation/1.0"}
    if payload is not None:
        headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "MCP-Protocol-Version": "2025-03-26",
            }
        )
    req = Request(
        url, data=json.dumps(payload).encode() if payload else None, headers=headers
    )
    with NET, urlopen(req, timeout=35) as response:
        data = response.read(4_000_001)
        if len(data) > 4_000_000:
            raise ValueError("Response exceeds the documentation size limit")
        return data


def mcp(name, repo):
    global MCP_LAST
    with MCP_LOCK:
        delay = max(0, MCP_LAST + 1.1 - time.monotonic())
        if delay:
            time.sleep(delay)
        MCP_LAST = time.monotonic()
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": {"repository": f"{OWNER}/{repo}"}},
    }
    raw = request("https://gitdiagram.com/mcp", payload).decode("utf-8")
    if raw.lstrip().startswith("{"):
        answer = json.loads(raw)
    else:
        events = [
            json.loads(line[5:].strip())
            for line in raw.splitlines()
            if line.startswith("data:")
        ]
        answer = next((item for item in events if item.get("id") == 1), None)
        if answer is None:
            raise ValueError("GitDiagram returned no matching protocol response")
    if "error" in answer or answer.get("result", {}).get("isError"):
        raise ValueError("GitDiagram returned a protocol, service or rate-limit error")
    return answer["result"]


def source_candidate(entry):
    path = PurePosixPath(entry["path"])
    if entry.get("type") != "blob" or entry.get("mode") == "120000":
        return False
    if (
        path.is_absolute()
        or ".." in path.parts
        or any(p.lower() in EXCLUDED for p in path.parts)
    ):
        return False
    if any(p.startswith(".env") or p in {".pypirc", "dump.rdb"} for p in path.parts):
        return False
    if path.name.endswith((".min.js", ".d.ts", ".generated.cs", ".g.cs")):
        return False
    readme = path.name.lower().startswith("readme") and path.suffix.lower() in {
        "",
        ".md",
        ".markdown",
        ".txt",
        ".rst",
        ".adoc",
        ".rdoc",
    }
    return path.suffix.lower() in LANGUAGES or path.name in MANIFESTS or readme


def fetch_blob(repo, commit, entry, offline):
    path = CACHE / "blobs" / entry["sha"]
    if path.exists():
        data = path.read_bytes()
    elif offline:
        raise FileNotFoundError("Source blob was not cached")
    else:
        url = f"https://raw.githubusercontent.com/{OWNER}/{quote(repo)}/{commit}/{quote(entry['path'])}"
        data = request(url)
    expected = hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\0" + data
    ).hexdigest()
    if expected != entry["sha"]:
        raise ValueError("Source blob integrity check failed")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return data.decode("utf-8")


def node_text(node, source):
    return source[node.start_byte : node.end_byte].decode("utf-8", errors="replace")


def walk(node):
    yield node
    for child in node.named_children:
        yield from walk(child)


def identifier(node, source):
    if node is None:
        return None
    name = node.child_by_field_name("name") or node.child_by_field_name("declarator")
    if name is not None and name != node:
        return identifier(name, source)
    if node.type in {"class_declaration", "function_declaration"}:
        direct = next(
            (
                child
                for child in node.named_children
                if child.type in {"type_identifier", "simple_identifier"}
            ),
            None,
        )
        if direct:
            return node_text(direct, source)
    value = node_text(node, source)
    return value if re.fullmatch(r"[A-Za-z_]\w*", value) else None


def declared_bases(node, source, language):
    # Only explicit inheritance syntax is used. Imports/co-location are not inheritance.
    values = []
    if language == "python":
        bases = node.child_by_field_name("superclasses")
        if bases:
            values = [
                node_text(n, source)
                for n in bases.named_children
                if n.type in {"identifier", "attribute", "subscript"}
            ]
    elif language == "cpp":
        bases = next(
            (n for n in node.named_children if n.type == "base_class_clause"), None
        )
        if bases:
            values = [
                node_text(n, source)
                for n in bases.named_children
                if n.type
                in {"type_identifier", "qualified_identifier", "template_type"}
            ]
    else:
        # Stop at a generic's outer type: its arguments are not additional bases.
        def collect(clause):
            if clause.type in {"type_arguments", "type_parameters", "value_arguments"}:
                return
            if clause.type in {
                "type_identifier",
                "identifier",
                "name",
                "qualified_name",
                "constant",
            }:
                values.append(node_text(clause, source))
                return
            if clause.type in {
                "generic_type",
                "generic_name",
                "user_type",
                "template_type",
            }:
                if clause.named_children:
                    collect(clause.named_children[0])
                return
            for child in clause.named_children:
                collect(child)

        kinds = {
            "superclass",
            "super_interfaces",
            "base_list",
            "class_heritage",
            "extends_type_clause",
            "base_clause",
            "class_interface_clause",
            "delegation_specifier",
        }
        for clause in (n for n in node.named_children if n.type in kinds):
            collect(clause)
    return list(
        dict.fromkeys(
            v for v in values if len(v) <= 100 and not re.search(r"[\n\"<>]", v)
        )
    )


def extract_types(path, text):
    from tree_sitter_language_pack import get_parser

    language = LANGUAGES.get(PurePosixPath(path).suffix.lower())
    if not language:
        return [], None
    source = text.encode("utf-8")
    parser = get_parser(language)
    tree = parser.parse(source)
    found = []
    for node in walk(tree.root_node):
        kind = DECLARATIONS.get(node.type)
        if language == "go" and node.type == "type_spec":
            underlying = node.child_by_field_name("type")
            if underlying and underlying.type in {"struct_type", "interface_type"}:
                kind = "struct" if underlying.type == "struct_type" else "interface"
        if not kind or node.is_missing:
            continue
        name = identifier(node, source)
        if not name:
            continue
        body = node.child_by_field_name("body")
        if language in {"c", "cpp"} and body is None:
            continue  # struct Foo* is a type reference, not a new type definition.
        if language == "kotlin" and body is None:
            body = next(
                (child for child in node.named_children if child.type == "class_body"),
                None,
            )
        methods = []
        if body:
            for member in body.named_children:
                if member.type == "decorated_definition":
                    member = member.child_by_field_name("definition") or member
                if member.type in METHODS:
                    method = identifier(member, source)
                    if method:
                        methods.append(method)
                elif language == "cpp" and member.type == "field_declaration":
                    declarator = member.child_by_field_name("declarator")
                    if declarator and declarator.type == "function_declarator":
                        method = identifier(declarator, source)
                        if method:
                            methods.append(method)
        line = node.start_point.row + 1
        found.append(
            {
                "id": "t"
                + hashlib.sha256(f"{path}:{line}:{name}".encode()).hexdigest()[:12],
                "name": name,
                "kind": kind,
                "file": path,
                "line": line,
                "language": language,
                "methods": list(dict.fromkeys(methods)),
                "bases": declared_bases(node, source, language),
            }
        )
    # Rust methods live in impl blocks, not inside struct declarations.
    if language == "rust":
        for node in walk(tree.root_node):
            if node.type != "impl_item" or node.has_error:
                continue
            target = node.child_by_field_name("type")
            name = node_text(target, source) if target else ""
            match = next((item for item in found if item["name"] == name), None)
            body = node.child_by_field_name("body")
            if match and body:
                for child in body.named_children:
                    if child.type == "function_item":
                        method = identifier(child, source)
                        if method and method not in match["methods"]:
                            match["methods"].append(method)
    if language == "go":
        for node in walk(tree.root_node):
            if node.type != "method_declaration" or node.has_error:
                continue
            receiver = node.child_by_field_name("receiver")
            if receiver:
                receiver_types = [
                    node_text(n, source)
                    for n in walk(receiver)
                    if n.type == "type_identifier"
                ]
                match = next(
                    (item for item in found if item["name"] in receiver_types), None
                )
                method = identifier(node, source)
                if match and method and method not in match["methods"]:
                    match["methods"].append(method)
    return found, "syntax-errors" if tree.root_node.has_error else None


def class_diagram(types, method_limit=None):
    lines = ["classDiagram", "direction TB"]
    external = {}
    for item in types:
        lines.append(f'class {item["id"]}["{item["name"]}"] {{')
        if item["kind"] != "class":
            lines.append(f"  <<{item['kind']}>>")
        methods = (
            item["methods"] if method_limit is None else item["methods"][:method_limit]
        )
        lines.extend(f"  {method}()" for method in methods)
        lines.append("}")
    for item in types:
        for base in item["bases"]:
            matches = [
                t for t in types if t["name"] == base and t["file"] == item["file"]
            ]
            if len(matches) == 1:
                parent = matches[0]["id"]
            else:
                key = (item["file"], base)
                if key not in external:
                    parent = "b" + hashlib.sha256(repr(key).encode()).hexdigest()[:12]
                    external[key] = parent
                    lines.append(
                        f'class {parent}["{base}"] {{\n  <<unresolved_base>>\n}}'
                    )
                parent = external[key]
            if len(matches) == 1 and matches[0]["kind"] in {"interface", "trait"}:
                lines.append(f"{parent} <|.. {item['id']}")
            elif len(matches) == 1 or item.get("language") in {"python", "cpp", "c"}:
                lines.append(f"{parent} <|-- {item['id']}")
            else:
                lines.append(f"{item['id']} ..> {parent} : declared base")
    return "\n".join(lines) + "\n"


def install_blocks(path, text):
    heading = ""
    headings = []
    result = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r"^(#+)\s+(.*)", line)
        if match:
            heading = match[2]
            headings = headings[: len(match[1]) - 1] + [heading]
        if not line.startswith("```"):
            i += 1
            continue
        start = i
        allowed = bool(
            re.search(
                r"install|setup|quick.?start|getting.?started|build|running|usage|utilis|compil",
                " / ".join(headings),
                re.IGNORECASE,
            )
            and re.match(r"^```(?:bash|sh|shell|console|powershell|ps1|zsh)?\s*$", line)
        )
        commands = []
        excluded = False
        i += 1
        while i < len(lines):
            value = lines[i]
            i += 1
            if value.startswith("```"):
                break
            # Never republish literal credential assignments or remote pipe-to-shell recipes.
            if re.search(
                r"(?:token|secret|password|api.?key|credential)\s*[:=]|(?:curl|wget).*\|",
                value,
                re.IGNORECASE,
            ):
                excluded = True
                continue
            if value.strip() and not value.lstrip().startswith("#"):
                commands.append(value)
        if (
            allowed
            and commands
            and not excluded
            and not re.search(r"uninstall|désinstall|remov", heading, re.IGNORECASE)
        ):
            result.append(
                {
                    "file": path,
                    "line": start + 1,
                    "heading": heading,
                    "commands": "\n".join(commands[:12]),
                }
            )
    return result[:5]


def manifest_info(path, text):
    if PurePosixPath(path).name != "package.json":
        return None
    try:
        package = json.loads(text)
    except ValueError:
        return None
    if not isinstance(package, dict) or not isinstance(
        package.get("scripts", {}), dict
    ):
        return None
    scripts = [
        {"name": key, "command": value}
        for key, value in package.get("scripts", {}).items()
        if key in {"dev", "build", "start", "test", "lint", "typecheck"}
        and isinstance(value, str)
        and len(value) < 500
        and not re.search(
            r"(?:token|secret|password|api.?key)\s*[:=]", value, re.IGNORECASE
        )
    ]
    return {"file": path, "engines": package.get("engines", {}), "scripts": scripts}


def repo_articles(notes):
    names = {note["repo"].lower(): note["repo"] for note in notes}
    aliases = {
        "moonlight-n3ds": "Artemis-N3DS",
        "sm64coopdx-switch": "sm64coopdx-switch-N3DS",
    }
    index = {note["repo"]: [] for note in notes}
    count = 0
    for source in sorted((ROOT / "hugo/content").rglob("*.md")):
        text = source.read_text(encoding="utf-8")
        count += 1
        refs = {
            match.lower().removesuffix(".git")
            for match in re.findall(
                r"https://github\.com/antoinebou12/([\w.\-]+)", text
            )
        }
        explicit = re.search(r'^repository_note:\s*"([^"]+)"', text, re.MULTILINE)
        if explicit:
            refs.add(explicit[1].lower())
        title = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', text, re.MULTILINE)
        for ref in refs:
            name = names.get(ref) or aliases.get(ref)
            if name in index:
                relative = source.relative_to(ROOT / "hugo/content").as_posix()
                index[name].append(
                    {
                        "path": relative,
                        "title": title[1] if title else source.stem,
                        "lang": "fr" if source.name.endswith(".fr.md") else "en",
                    }
                )
    return {"markdown_files_read": count, "repositories": index}


def import_gitdiagram(repo, slug, paths, offline):
    cached = CACHE / slug / "gitdiagram.json"
    if offline:
        return load(cached, {"status": "not_checked"})
    result = {
        "url": f"https://gitdiagram.com/{OWNER}/{quote(repo)}",
    }
    try:
        response = mcp("get_repository_diagram", repo)
        view = response.get("_meta", {}).get("com.gitdiagram/diagram", {})
        if view.get("repository", "").lower() != f"{OWNER}/{repo}".lower():
            raise ValueError("GitDiagram repository mismatch")
        if view.get("status") == "found" and isinstance(view.get("mermaid"), str):
            source = view["mermaid"]
            output = EXPORT / slug / "gitdiagram.mmd"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(source, encoding="utf-8")
            linked = re.findall(
                r'https://github\.com/[^/]+/[^/]+/(?:blob|tree)/[^/]+/([^"\s]+)', source
            )
            stale = sorted(
                {
                    path.rstrip("/")
                    for path in linked
                    if path.rstrip("/") not in paths
                    and not any(p.startswith(path.rstrip("/") + "/") for p in paths)
                }
            )
            unsafe = bool(
                re.search(
                    r"%%\s*\{|^---|<\s*(?:script|iframe)|javascript:",
                    source,
                    re.IGNORECASE | re.MULTILINE,
                )
            )
            clean = "\n".join(
                line
                for line in source.splitlines()
                if not re.match(r"\s*(?:click|classDef|style|linkStyle)\s", line)
            )
            clean = re.sub(r":::[\w-]+", "", clean)
            result.update(
                status="needs_review" if stale or unsafe else "available",
                missing_paths=stale,
                source_file=f"repository-docs/{slug}/gitdiagram.mmd",
                mermaid=None if unsafe else clean,
                linked_paths=len(linked),
            )
        else:
            result["status"] = "missing"
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
        result.update(status="unavailable", error=type(exc).__name__)
    save(cached, result)
    return result


def analyze(note, args):
    repo, slug = note["repo"], note["slug"]
    metadata_file = CACHE / slug / "inputs.json"
    if args.offline:
        inputs = load(metadata_file)
        if not inputs:
            raise FileNotFoundError("No cached repository snapshot")
    else:
        metadata = github(f"repos/{OWNER}/{repo}")
        if metadata.get("private") or metadata.get("visibility") != "public":
            raise ValueError("Only public repositories may be documented")
        branch = github(
            f"repos/{OWNER}/{repo}/branches/{quote(metadata['default_branch'], safe='')}"
        )
        commit = branch["commit"]["sha"]
        tree = github(f"repos/{OWNER}/{repo}/git/trees/{commit}?recursive=1")
        inputs = {
            "metadata": metadata,
            "tree": tree,
            "commit": commit,
            "languages": github(f"repos/{OWNER}/{repo}/languages"),
            "fetched_at": datetime.now(UTC).isoformat(),
        }
        save(metadata_file, inputs)
    tree = inputs["tree"]
    commit = inputs["commit"]
    entries = [e for e in tree["tree"] if source_candidate(e)]
    eligible = len(entries)
    entries.sort(
        key=lambda e: (
            e["path"] not in note["files"],
            len(PurePosixPath(e["path"]).parts),
            e["path"],
        )
    )
    oversized = [e for e in entries if e.get("size", 0) > MAX_BYTES]
    entries = [e for e in entries if e.get("size", 0) <= MAX_BYTES]
    if args.max_files:
        entries = entries[: args.max_files]
    texts, failures = {}, []
    with ThreadPoolExecutor(max_workers=8) as pool:
        jobs = {
            pool.submit(fetch_blob, repo, commit, entry, args.offline): entry
            for entry in entries
        }
        for future in as_completed(jobs):
            entry = jobs[future]
            try:
                texts[entry["path"]] = future.result()
            except (OSError, ValueError, RuntimeError) as exc:
                failures.append({"file": entry["path"], "error": type(exc).__name__})
    types, parse_errors, installation, manifests = [], [], [], []
    parser_unavailable = set()
    for path, text in sorted(texts.items()):
        if PurePosixPath(path).name.lower().startswith("readme"):
            installation.extend(install_blocks(path, text))
        if PurePosixPath(path).name in MANIFESTS:
            info = manifest_info(path, text)
            if info:
                manifests.append(info)
        language = LANGUAGES.get(PurePosixPath(path).suffix.lower())
        if language and language not in parser_unavailable:
            try:
                if args.verbose:
                    print(f"  Parsing {repo}/{path}", flush=True)
                items, error = extract_types(path, text)
                types.extend(items)
                if error:
                    parse_errors.append({"file": path, "error": error})
            except (ImportError, ValueError, RuntimeError, TypeError) as exc:
                parse_errors.append({"file": path, "error": type(exc).__name__})
    types.sort(key=lambda t: (t["file"] not in note["files"], t["file"], t["line"]))
    source_url = f"https://github.com/{OWNER}/{quote(repo)}/blob/{commit}/"
    previous = load(EXPORT / slug / "analysis.json", {})
    per_file = []
    for path in sorted({t["file"] for t in types}):
        items = [t for t in types if t["file"] == path]
        filename = "classes/" + hashlib.sha256(path.encode()).hexdigest()[:16] + ".mmd"
        output = EXPORT / slug / filename
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(class_diagram(items), encoding="utf-8")
        per_file.append(
            {
                "path": path,
                "types": len(items),
                "source_url": source_url + quote(path),
                "download": f"repository-docs/{slug}/{filename}",
            }
        )
    # Remove only stale diagrams listed in our previous generated analysis.
    current = {entry["download"] for entry in per_file}
    for entry in previous.get("class_files", []):
        old = entry.get("download", "")
        if old not in current and re.fullmatch(
            rf"repository-docs/{re.escape(slug)}/classes/[0-9a-f]{{16}}\.mmd", old
        ):
            target = (ROOT / "hugo/static" / old).resolve()
            if target.is_relative_to(EXPORT.resolve()):
                target.unlink(missing_ok=True)
    source_manifest = [
        {
            "path": entry["path"],
            "blob_sha": entry["sha"],
            "source_url": source_url + quote(entry["path"]),
        }
        for entry in entries
        if entry["path"] in texts
    ]
    file_map = ["flowchart TD", f'  root["{repo}"]']
    for index, entry in enumerate(source_manifest[:16]):
        label = (
            entry["path"]
            .replace('"', "#quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        file_map.extend([f'  f{index}["{label}"]', f"  root --> f{index}"])
    file_map_source = "\n".join(file_map) + "\n"
    file_map_path = EXPORT / slug / "files.mmd"
    file_map_path.parent.mkdir(parents=True, exist_ok=True)
    file_map_path.write_text(file_map_source, encoding="utf-8")
    total = sum(inputs["languages"].values())
    languages = (
        [
            {"name": name, "bytes": size, "percent": round(size / total * 100, 2)}
            for name, size in sorted(
                inputs["languages"].items(), key=lambda pair: -pair[1]
            )
        ]
        if total
        else []
    )
    analysis = {
        "repo": repo,
        "slug": slug,
        "commit": commit,
        "source_url": source_url,
        "tree_url": f"https://github.com/{OWNER}/{quote(repo)}/tree/{commit}",
        "fetched_at": inputs["fetched_at"],
        "languages": languages,
        "language_bytes": total,
        "coverage": {
            "tree_files": sum(e["type"] == "blob" for e in tree["tree"]),
            "eligible_files": eligible,
            "read_files": len(texts),
            "oversized_files": len(oversized),
            "truncated_tree": tree.get("truncated", False),
            "limited": bool(args.max_files and eligible > args.max_files),
            "failures": failures,
            "parse_errors": parse_errors,
            "unavailable_parsers": sorted(parser_unavailable),
        },
        "installation": installation[:8],
        "manifests": manifests[:10],
        "type_count": len(types),
        "types": types,
        "class_files": per_file,
        "source_manifest": source_manifest,
        "file_overview": file_map_source,
        "file_overview_count": min(16, len(source_manifest)),
        "class_overview": class_diagram(types[:12], method_limit=4) if types else None,
        "overview_types": min(12, len(types)),
        "gitdiagram": import_gitdiagram(
            repo, slug, {e["path"] for e in tree["tree"]}, args.offline
        ),
    }
    export = EXPORT / slug / "analysis.json"
    save(export, analysis)
    return analysis


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo", action="append", help="Repository name; repeat to select several"
    )
    parser.add_argument(
        "--offline", action="store_true", help="Use cached verified inputs only"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print file-level parsing progress"
    )
    parser.add_argument(
        "--gitdiagram-only",
        action="store_true",
        help="Refresh external exports without re-reading source",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=0,
        help="Optional explicit cap; 0 reads all eligible files",
    )
    args = parser.parse_args()
    if args.max_files < 0:
        parser.error("--max-files must be nonnegative")
    notes = load(ROOT / "hugo/data/repository_notes.json")["notes"]
    if args.repo and set(args.repo) - {n["repo"] for n in notes}:
        parser.error("Unknown repository; only the public site inventory is accepted")
    selected = [n for n in notes if not args.repo or n["repo"] in args.repo]
    prior = load(DATA, {"schema_version": 1, "repositories": {}})
    errors = []
    for note in selected:
        try:
            print(f"Inspecting {note['repo']}...", flush=True)
            if args.gitdiagram_only:
                value = prior["repositories"][note["repo"]]
                inputs = load(CACHE / note["slug"] / "inputs.json")
                value["gitdiagram"] = import_gitdiagram(
                    note["repo"],
                    note["slug"],
                    {entry["path"] for entry in inputs["tree"]["tree"]},
                    args.offline,
                )
                save(EXPORT / note["slug"] / "analysis.json", value)
            else:
                value = analyze(note, args)
            prior["repositories"][note["repo"]] = value
            save(DATA, prior)
            coverage = value["coverage"]
            print(
                f"{note['repo']}: {coverage['read_files']}/{coverage['eligible_files']} files, "
                f"{value['type_count']} types, GitDiagram={value['gitdiagram']['status']}",
                flush=True,
            )
        except (
            OSError,
            ValueError,
            RuntimeError,
            KeyError,
            TypeError,
            subprocess.SubprocessError,
        ) as exc:
            errors.append({"repo": note["repo"], "error": type(exc).__name__})
            print(
                f"{note['repo']}: failed ({type(exc).__name__}); previous output preserved",
                flush=True,
            )
    save(ROOT / "hugo/data/repository_article_index.json", repo_articles(notes))
    save(CACHE / "last-run.json", {"errors": errors, "selected": len(selected)})
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
