"""UML source generation and SVG sanitizing. No remote calls."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

SPEC = spec_from_file_location("repository_uml", Path(__file__).parents[1] / "build/repository_uml.py")
uml = module_from_spec(SPEC)
SPEC.loader.exec_module(uml)

DOSSIER = {
    "public": {
        "routes": [{"method": "GET", "path": "/admin/users"}, {"method": "POST", "path": "/admin/users"}, {"method": "GET", "path": "/health"}],
        "mcp": [{"kind": "tool", "name": "generate_diagram"}],
        "cli": [],
        "cli_total": 0,
        "entry_points": [{"kind": "console script", "name": "demo"}],
    },
    "flow": {"groups": [{"label": "Runtime"}, {"label": "Rendering"}]},
    "modules": {"items": [{"name": "core"}]},
    "integrations": {"services": [{"label": ["Kroki", "Kroki"]}]},
    "database": {"engines": [{"label": ["SQLite", "SQLite"], "kind": "sql"}]},
    "services": {"hosting": [{"label": ["Docker image", "Image Docker"]}], "containers": ["api", "kroki"], "base_images": [{"image": "python:3.13-slim"}]},
    "tests": {
        "workflows": [
            {
                "name": "CI",
                "jobs": [
                    {"name": "lint", "needs": [], "steps": ["Checkout", "Ruff"]},
                    {"name": "test", "needs": [], "steps": ["Checkout", "pytest"]},
                    {"name": "deploy", "needs": ["lint", "test"], "steps": ["Publish: site"]},
                ],
            }
        ]
    },
}


def test_usecase_links_actors_to_route_groups_tools_and_commands():
    source = uml.usecase_uml("demo", DOSSIER, False)
    assert 'actor "HTTP client" as A_http' in source
    assert 'usecase "GET/POST /admin (2 routes)" as U0' in source
    assert 'usecase "Tool generate_diagram"' in source
    assert 'usecase "Run demo"' in source
    assert "A_mcp --> U2" in source


def test_component_offers_interfaces_and_depends_on_externals():
    source = uml.component_uml("demo", DOSSIER, True)
    assert 'interface "Client HTTP" as P0' in source
    assert 'component "Runtime" as C0' in source
    assert "SYS ..> R0 : utilise" in source
    assert 'database "SQLite" as S0' in source


def test_deployment_uses_compose_services_and_base_images():
    source = uml.deployment_uml("demo", DOSSIER, False)
    assert 'node "Docker Compose" as H {' in source
    assert 'node "api" as N0 <<container>>' in source
    assert "IMG0 ..> N0 : builds" in source
    assert "N0 --> DB0" in source


def test_activity_forks_parallel_jobs_then_runs_dependants():
    source = uml.activity_uml("demo", DOSSIER, False)
    assert source.index("fork") < source.index("end fork") < source.index('partition "deploy"')
    assert ":Publish  site;" in source


def test_diagrams_are_skipped_without_evidence():
    empty = {
        "public": {"routes": [], "mcp": [], "cli": [], "cli_total": 0, "entry_points": []},
        "flow": None, "modules": {"items": []},
        "integrations": {"services": []}, "database": {"engines": []},
        "services": {"hosting": [], "containers": [], "base_images": []},
        "tests": {"workflows": []},
    }
    assert [build("x", empty, False) for _, _, build, _, _ in uml.DIAGRAMS] == [None, None, None, None]


def test_sanitize_strips_executable_markup():
    raw = (
        '<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"><?plantuml 1.2025?>'
        '<script>alert(2)</script><foreignObject><div>x</div></foreignObject>'
        '<a href="javascript:alert(3)"><rect onclick="x()" width="1"/></a><!-- source --></svg>'
    )
    clean = uml.sanitize(raw)
    for needle in ("onload", "<script", "foreignObject", "javascript:", "onclick", "plantuml", "source"):
        assert needle not in clean
    assert '<rect width="1"/>' in clean


def test_sanitize_rejects_non_svg():
    with pytest.raises(ValueError):
        uml.sanitize("<html>error</html>")


def test_labels_cannot_break_plantuml_syntax():
    assert uml.q('a"b{c}|d;e') == "a'b'c''d'e"
