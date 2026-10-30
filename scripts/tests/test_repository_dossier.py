"""Deterministic dossier extraction tests. No remote calls or repository code execution."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

SPEC = spec_from_file_location(
    "repository_dossier", Path(__file__).parents[1] / "build/repository_dossier.py"
)
dossier = module_from_spec(SPEC)
SPEC.loader.exec_module(dossier)

ANALYSIS = {
    "source_url": "https://github.com/o/r/blob/c/",
    "tree_url": "https://github.com/o/r/tree/c",
    "languages": [{"name": "Python", "percent": 100.0}],
}


def test_measured_coverage_ignores_thresholds_and_invalid_totals():
    texts = {
        "coverage-summary.json": '{"total":{"lines":{"total":20,"covered":15}}}',
        "coverage.xml": '<coverage lines-valid="10" lines-covered="9">',
        "lcov.info": 'LF:10\nLH:5\nLF:10\nLH:10\n',
        "pyproject.toml": 'fail_under = 95',
        "bad/coverage.json": '{"totals":{"num_statements":5,"covered_lines":8}}',
    }
    reports = dossier.coverage_reports(ANALYSIS, texts)
    assert [r["percent"] for r in reports] == [75, 90, 75]
    assert all(r["url"].startswith(ANALYSIS["source_url"]) for r in reports)


@pytest.mark.parametrize(
    ("path", "layer"),
    [
        ("tests/test_api.py", "tests"),
        ("frontend/src/components/Button.tsx", "presentation"),
        ("app/api/routes.py", "interface"),
        ("src/services/billing.py", "application"),
        ("src/models/user.py", "domain"),
        ("pkg/db/session.py", "infrastructure"),
        (".github/workflows/ci.yml", "hosting"),
        ("Dockerfile", "hosting"),
        ("pkg/util.py", "core"),
    ],
)
def test_layer_of(path, layer):
    assert dossier.layer_of(path) == layer


def test_module_key_skips_generic_folders():
    assert dossier.module_key("src/main/java/billing/Invoice.java") == ("billing", "src/main/java/billing")
    assert dossier.module_key("mcp_core/core/config.py") == ("mcp_core/core", "mcp_core/core")
    assert dossier.module_key("main.py") == ("(root)", "")


def test_ide_folders_are_not_sources():
    assert not dossier.is_source("android/.idea/misc.xml")
    assert dossier.is_source("android/app/src/main/res/layout/main.xml")


def test_routes_mcp_and_cli_are_public_interface():
    texts = {
        "app.py": (
            "from fastapi import FastAPI\napp = FastAPI()\n"
            "@app.get('/health')\ndef health(): ...\n"
            "@app.post(\"/render\")\ndef render(): ...\n"
        ),
        "server.py": "from fastmcp import FastMCP\nmcp = FastMCP()\n@mcp.tool()\nasync def generate_diagram(x): ...\n",
        "cli.py": "parser.add_argument('--format')\nsub.add_parser('render')\n",
    }
    result = dossier.build_public(ANALYSIS, texts, [], [])
    assert {(r["method"], r["path"]) for r in result["routes"]} == {("GET", "/health"), ("POST", "/render")}
    assert [t["name"] for t in result["mcp"]] == ["generate_diagram"]
    assert {c["name"] for c in result["cli"]} == {"--format", "render"}
    assert result["routes"][0]["url"].startswith("https://github.com/o/r/blob/c/app.py#L")
    assert {r["path"]: r["ops"] for r in result["routes"]} == {"/health": True, "/render": False}


def test_private_interface_counts_underscore_helpers():
    texts = {"core.py": "def _helper():\n    pass\n\ndef public():\n    pass\n"}
    result = dossier.build_private(ANALYSIS, texts)
    assert result["counts"][0]["count"] == 1
    assert result["examples"][0]["name"] == "_helper"


def test_entities_from_dataclass_and_pydantic():
    text = (
        "from dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: int\n    y: int\n\n"
        "class User(BaseModel):\n    name: str\n    email: str = ''\n"
    )
    types = [
        {"name": "Point", "kind": "class", "file": "models.py", "line": 4, "language": "python", "methods": [], "bases": []},
        {"name": "User", "kind": "class", "file": "models.py", "line": 8, "language": "python", "methods": [], "bases": ["BaseModel"]},
    ]
    result = dossier.build_entities(ANALYSIS, {"models.py": text}, types)
    found = {e["name"]: (e["kind"], e["fields"]) for e in result["items"]}
    assert found == {"Point": ("dataclass", ["x", "y"]), "User": ("schema", ["name", "email"])}


def test_database_ignores_plain_words_and_finds_tables():
    texts = {
        "icons.py": "ICONS = ['postgres', 'redis', 'mysql']\n",
        "db.py": "import sqlite3\nconn.execute('CREATE TABLE IF NOT EXISTS runs (id INTEGER)')\n",
    }
    result = dossier.build_database(ANALYSIS, texts, list(texts))
    assert [e["name"] for e in result["engines"]] == ["SQLite"]
    assert [t["name"] for t in result["tables"]] == ["runs"]


def test_stack_reads_manifests_without_values():
    texts = {
        "pyproject.toml": '[project]\nrequires-python = ">=3.12"\ndependencies = ["httpx>=0.27", "pydantic"]\n',
        "package.json": '{"dependencies": {"react": "^19.0.0"}, "devDependencies": {"vitest": "^3"}, "engines": {"node": ">=20"}}',
    }
    result = dossier.build_stack(ANALYSIS, texts)
    by_file = {m["file"]: m for m in result["manifests"]}
    assert [d["name"] for d in by_file["pyproject.toml"]["runtime"]] == ["httpx", "pydantic"]
    assert by_file["pyproject.toml"]["toolchain"] == ["Python >=3.12"]
    assert by_file["package.json"]["dev"][0]["name"] == "vitest"
    assert by_file["package.json"]["toolchain"] == ["node >=20"]


def test_security_reports_env_names_only():
    texts = {"settings.py": "import os\nTOKEN = os.environ['API_TOKEN']\nDEBUG = os.getenv('APP_DEBUG')\n"}
    result = dossier.build_security(ANALYSIS, texts, list(texts))
    names = [v["name"] for v in result["env_vars"]]
    assert names == ["API_TOKEN", "APP_DEBUG"]
    assert result["env_vars"][0]["secret"] is True
    assert "os.environ" not in str(result["env_vars"])


def test_tests_section_counts_cases_and_frameworks():
    texts = {"tests/test_core.py": "import pytest\n\ndef test_a():\n    pass\n\ndef test_b():\n    pass\n"}
    result = dossier.build_tests(ANALYSIS, texts, ["tests/test_core.py", "core.py"])
    assert (result["files"], result["cases"]) == (1, 2)
    assert [f["name"] for f in result["frameworks"]] == ["pytest"]


def test_gitdiagram_edges_become_ordered_flow():
    analysis = dict(
        ANALYSIS,
        gitdiagram={
            "status": "available",
            "url": "https://gitdiagram.com/o/r",
            "mermaid": (
                "flowchart TD\n"
                'subgraph g["Runtime"]\n  node_server["MCP Server<br/>[server.py]"]\nend\n'
                'node_client(("AI Client"))\nnode_kroki["Kroki"]\n'
                'node_server -->|"renders"| node_kroki\n'
                'node_client -->|"requests tools"| node_server\n'
            ),
        },
    )
    flow = dossier.parse_gitdiagram(analysis, ["src/server.py"])
    assert [(s["from"], s["to"]) for s in flow["steps"]] == [("AI Client", "MCP Server"), ("MCP Server", "Kroki")]
    assert flow["groups"][0]["nodes"][0]["path"] == "src/server.py"
    assert flow["entry_points"] == ["AI Client"]


def test_layers_mermaid_is_bilingual():
    layers = dossier.build_layers(ANALYSIS, ["api/routes.py", "models/user.py", "tests/test_x.py"], [])
    en, fr = dossier.layers_mermaid(layers, "en"), dossier.layers_mermaid(layers, "fr")
    assert 'L_interface["Entry points and API"]' in en
    assert "Points d’entrée et API" in fr
    assert "L_interface ~~~ L_domain" in en


def test_entity_diagram_links_fields_to_other_entities():
    text = (
        "class Order(BaseModel):\n    id: int\n    items: list[Item]\n\n"
        "class Item(BaseModel):\n    sku: str\n"
    )
    types = [
        {"name": "Order", "kind": "class", "file": "m.py", "line": 1, "language": "python", "methods": [], "bases": ["BaseModel"]},
        {"name": "Item", "kind": "class", "file": "m.py", "line": 5, "language": "python", "methods": [], "bases": ["BaseModel"]},
    ]
    diagram = dossier.build_entities(ANALYSIS, {"m.py": text}, types)["diagram"]
    assert "+list~Item~ items" in diagram
    assert " --> " in diagram and ": items" in diagram


def test_route_map_groups_by_first_segment():
    routes = [{"method": "GET", "path": p} for p in ("/admin/users", "/admin/settings", "/health", "/")]
    diagram = dossier.route_mermaid(routes)
    assert diagram.startswith("flowchart LR")
    assert '"/admin"' in diagram and "GET /admin/users" in diagram


def test_sequence_diagram_keeps_walk_order():
    steps = [
        {"from": "Client", "to": "Server", "label": "calls: tool", "async": False},
        {"from": "Server", "to": "Kroki", "label": "renders", "async": True},
    ]
    diagram = dossier.sequence_mermaid(steps)
    assert "participant P0 as Client" in diagram
    assert "P0->>P1: calls  tool" in diagram
    assert "P1--)P2: renders" in diagram


def test_context_diagram_puts_callers_left_and_dependencies_right():
    public = {"routes": [{"path": "/"}], "mcp": [], "cli": [], "entry_points": []}
    integrations = {"services": [{"label": ["Kroki", "Kroki"]}], "hosts": []}
    database = {"engines": [{"label": ["SQLite", "SQLite"]}]}
    services = {"hosting": [{"label": ["Docker image", "Image Docker"]}]}
    en = dossier.context_mermaid(public, integrations, database, services, "demo", "en")
    fr = dossier.context_mermaid(public, integrations, database, services, "demo", "fr")
    assert 'c0(["HTTP client"])' in en and "c0 --> sys" in en
    assert 'd1[("SQLite")]' in en
    assert "Image Docker" in fr


def test_gitdiagram_shapes_lose_their_brackets():
    analysis = dict(
        ANALYSIS,
        gitdiagram={
            "status": "available",
            "url": "https://gitdiagram.com/o/r",
            "mermaid": (
                "flowchart TD\n"
                'node_model["User model"]\nnode_db[("User persistence")]\nnode_ui(["Login page"])\n'
                'node_ui -->|"submits"| node_model\nnode_model -->|"persists"| node_db\n'
            ),
        },
    )
    flow = dossier.parse_gitdiagram(analysis, [])
    assert [(s["from"], s["to"]) for s in flow["steps"]] == [("Login page", "User model"), ("User model", "User persistence")]


def test_monitoring_finds_logging_errors_and_health_checks():
    texts = {
        "app.py": "import logging\nimport sentry_sdk\nlog = logging.getLogger(__name__)\n",
        "Dockerfile": "FROM python:3.13\nHEALTHCHECK CMD curl -f http://localhost/health\n",
    }
    routes = [{"method": "GET", "path": "/health"}, {"method": "GET", "path": "/users"}]
    result = dossier.build_monitoring(ANALYSIS, texts, routes)
    assert {s["name"] for s in result["signals"]} == {"Python logging", "Sentry"}
    assert [r["path"] for r in result["health_routes"]] == ["/health"]
    assert result["health_checks"][0]["label"] == "Docker HEALTHCHECK"


def test_deployment_reads_pipelines_triggers_and_targets():
    workflow = (
        "name: Release\non:\n  push:\n    tags: ['v*']\n  workflow_dispatch:\njobs:\n  publish:\n"
        "    environment: production\n    steps:\n      - uses: actions/checkout@v4\n"
        "      - name: Publish to PyPI\n        uses: pypa/gh-action-pypi-publish@release/v1\n"
    )
    services = {"hosting": [], "containers": [], "base_images": []}
    result = dossier.build_deployment(ANALYSIS, {".github/workflows/release.yml": workflow}, services)
    pipeline = result["pipelines"][0]
    assert pipeline["name"] == "Release"
    assert pipeline["triggers"] == ["push", "workflow_dispatch"]
    assert pipeline["environments"] == ["production"]
    assert pipeline["steps"] == ["Publish to PyPI"]
    assert [t["label"][0] for t in result["targets"]] == ["PyPI"]


@pytest.mark.parametrize(
    ("path", "text", "kind"),
    [
        ("tests/test_math.py", "def test_add(): pass", "unit"),
        ("tests/integration/test_api.py", "", "integration"),
        ("tests/test_routes.py", "client = TestClient(app)", "integration"),
        ("e2e/login.spec.ts", "", "e2e"),
        ("tests/ui.spec.ts", "import { test } from '@playwright/test'", "e2e"),
        ("benches/parse.rs", "", "benchmark"),
    ],
)
def test_test_files_are_classified_by_kind(path, text, kind):
    assert dossier.test_kind(path, text) == kind


def test_constructors_are_left_out_of_method_lists():
    t = {"name": "Client", "methods": ["__init__", "Client", "~Client", "send", "close"]}
    assert dossier.behaviour(t) == ["send", "close"]


def test_generated_code_and_workflow_expressions_are_left_out():
    assert dossier.generated({"file": "demo/pkg/mathlib.js", "methods": []})
    assert dossier.generated({"file": "src/lib.js", "methods": ["__wrap", "__destroy_into_raw"]})
    assert not dossier.generated({"file": "src/graph.rs", "methods": ["from_edges"]})
    jobs = dossier.workflow_jobs("jobs:\n  push:\n    steps:\n      - name: Push to NuGet.org (suffix ${{ matrix.suffix }})\n")
    assert jobs[0]["steps"] == ["Push to NuGet.org"]
    jobs = dossier.workflow_jobs("jobs:\n  build:\n    name: Host tests (${{ matrix.compiler }})\n")
    assert jobs[0]["title"] == "Host tests"
    assert dossier.workflow_jobs("jobs:\n  build:\n    name: ${{ matrix.name }}\n")[0]["title"] == "build"


def test_deploy_workflows_share_one_hosting_chip():
    texts = {f".github/workflows/{n}.yml": "jobs:\n  go:\n    steps:\n      - run: gh release create\n" for n in ("ci", "release")}
    hosting = dossier.build_services(ANALYSIS, texts, [], list(texts))["hosting"]
    assert [(h["label"][0], h["count"]) for h in hosting] == [("CI deploy workflow", 2)]
