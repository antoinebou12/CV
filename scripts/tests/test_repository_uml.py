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
    "layers": [
        {"key": "interface", "modules": [{"files": 4, "extensions": [".py"]}]},
        {"key": "core", "modules": [{"files": 9, "extensions": [".py"]}]},
    ],
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


def test_c4_context_shows_people_system_and_externals():
    source = uml.c4_context_uml("demo", dict(DOSSIER, _intro=["Demo renders diagrams. More text.", "Demo dessine."]), False)
    assert "!include <C4/C4_Context>" in source
    assert 'Person(P_http, "HTTP client")' in source
    assert 'System(SYS, "demo", "Demo renders diagrams")' in source
    assert 'System_Ext(E0, "Kroki")' in source and 'SystemDb(D0, "SQLite")' in source
    assert 'Rel(SYS, D0, "Reads and writes")' in source


def test_c4_container_uses_compose_services_or_layers():
    from_compose = uml.c4_container_uml("demo", DOSSIER, True)
    assert 'System_Boundary(SYS, "demo") {' in from_compose
    assert 'Container(C0, "api", "Docker")' in from_compose
    assert 'ContainerDb(DB0, "SQLite", "")' in from_compose
    layered = dict(DOSSIER, services=dict(DOSSIER["services"], containers=[]))
    source = uml.c4_container_uml("demo", layered, False)
    assert 'Container(APP, "demo", "Python")' in source
    assert 'Container(CORE' not in source
    assert 'Rel(API, CORE' not in source


def test_c4_sources_skip_plain_uml_styling():
    assert "skinparam" not in uml.wrap("Person(a, \"A\")", "c4plantuml")
    assert "skinparam" in uml.wrap("actor a", "usecase")


def test_compose_services_are_not_repeated_as_external_systems():
    source = uml.c4_container_uml("demo", DOSSIER, False)
    assert 'Container(C1, "kroki"' in source
    assert 'System_Ext(E0, "Kroki")' not in source


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
        "flow": None, "modules": {"items": []}, "layers": [],
        "integrations": {"services": []}, "database": {"engines": []},
        "services": {"hosting": [], "containers": [], "base_images": []},
        "tests": {"workflows": []},
    }
    assert [build("x", empty, False) for _, _, build, _, _ in uml.DIAGRAMS] == [None] * len(uml.DIAGRAMS)


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


def test_component_hierarchy_has_layers_and_languages_without_inferred_calls():
    source = uml.c4_component_uml("demo", DOSSIER, False)
    assert 'Boundary(L0, "interface", "layer")' in source
    assert 'Component(M0_0, "interface", "Python", "4 files")' in source
    assert 'Rel(' not in source


def test_code_groups_same_named_types_by_file_and_deduplicates_declarations():
    first = {"name": "Model", "file": "src/model.py", "fields": ["id"], "methods": ["save"]}
    other = {"name": "Model", "file": "api/model.py", "fields": ["name"]}
    dossier = dict(DOSSIER, logic={"types": [first, other]}, entities={"items": [first]})
    source = uml.c4_code_uml("demo", dossier, False)
    assert source.count('class "Model"') == 2
    assert 'package "src/model.py"' in source
    assert 'save()' in source
    assert '-->' not in source


def test_c4_compose_entry_is_the_project_service_and_transports_are_not_systems():
    dossier = dict(DOSSIER, integrations={"services": [{"label": ["Kroki", "Kroki"], "kind": "rendering"}, {"label": ["WebSocket", "WebSocket"], "kind": "transport"}]},
                   services=dict(DOSSIER["services"], containers=["kroki", "demo", "redis"]))
    source = uml.c4_container_uml("demo", dossier, False)
    assert 'Rel(P_http, C1, "Uses")' in source
    assert 'System_Ext(E0, "Kroki")' not in source
    assert "WebSocket" not in source
    assert 'Rel(C0, C1' not in source and 'Rel(C1, C2' not in source
