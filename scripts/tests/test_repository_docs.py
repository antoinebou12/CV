"""Deterministic extraction tests. No remote calls or repository code execution."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

SPEC = spec_from_file_location(
    "repository_docs", Path(__file__).parents[1] / "build/repository_docs.py"
)
docs = module_from_spec(SPEC)
SPEC.loader.exec_module(docs)


@pytest.mark.parametrize(
    ("path", "text", "expected"),
    [
        (
            "demo.py",
            'text = "class Fake: pass"\nclass Demo(Base):\n    def run(self): pass\n',
            {"Demo"},
        ),
        (
            "demo.cpp",
            "class Base {}; class Demo : public Base { public: void run(); }; struct Base* usage;",
            {"Base", "Demo"},
        ),
        (
            "demo.c",
            "struct Data { int value; }; struct Data* a; struct Data* b;",
            {"Data"},
        ),
        (
            "demo.cs",
            "interface IService { void Run(); } class Demo : IService { public void Run() {} }",
            {"IService", "Demo"},
        ),
        (
            "demo.ts",
            "class Demo<T> extends Base<T> implements Sink { run() {} }",
            {"Demo"},
        ),
        (
            "demo.java",
            "class Demo<T> extends Base<T> implements Runnable { public void run() {} }",
            {"Demo"},
        ),
        (
            "demo.rs",
            "pub struct State { value: u32 } impl State { pub fn run(&self) {} }",
            {"State"},
        ),
        ("demo.rb", "class Demo < Base\n  def run\n  end\nend\n", {"Demo"}),
        (
            "demo.go",
            "package main\ntype Service struct { name string }\nfunc (s Service) Run() {}",
            {"Service"},
        ),
        ("demo.sh", "echo class Fake", set()),
    ],
)
def test_type_extraction(path, text, expected):
    items, _ = docs.extract_types(path, text)
    assert {item["name"] for item in items} == expected
    assert all(item["line"] >= 1 and item["file"] == path for item in items)


@pytest.mark.parametrize(
    ("path", "text", "bases"),
    [
        ("demo.py", "class Demo(Base):\n    pass\n", ["Base"]),
        ("demo.cpp", "class Demo : public Base {};", ["Base"]),
        (
            "demo.ts",
            "class Demo<T> extends Base<T> implements Sink {}",
            ["Base", "Sink"],
        ),
        (
            "demo.java",
            "class Demo<T> extends Base<T> implements Runnable {}",
            ["Base", "Runnable"],
        ),
    ],
)
def test_generic_arguments_are_not_base_classes(path, text, bases):
    items, _ = docs.extract_types(path, text)
    assert items[0]["bases"] == bases


def test_rust_and_go_methods_are_attached_to_the_declared_type():
    rust, _ = docs.extract_types(
        "demo.rs", "struct State {} impl State { fn run(&self) {} }"
    )
    go, _ = docs.extract_types(
        "demo.go", "package main\ntype State struct {}\nfunc (s *State) Run() {}"
    )
    assert rust[0]["methods"] == ["run"]
    assert go[0]["methods"] == ["Run"]


def test_unrelated_types_do_not_acquire_fake_relationships():
    items, _ = docs.extract_types(
        "demo.py", "class One:\n    pass\nclass Two:\n    pass\n"
    )
    source = docs.class_diagram(items)
    assert "<|" not in source and "..>" not in source
    assert all(item["id"] in source for item in items)


def test_interface_realization_is_not_drawn_as_class_inheritance():
    items, _ = docs.extract_types("demo.cs", "interface I {} class C : I {}")
    assert "<|.." in docs.class_diagram(items)


def test_installation_fences_keep_their_context_and_do_not_consume_prose():
    source = "# Setup\n## Build\n```bash\nnpm ci\nnpm run build\n```\nDo not execute this prose.\n# Other\n```json\n{}\n```"
    blocks = docs.install_blocks("README.md", source)
    assert len(blocks) == 1
    assert blocks[0]["commands"] == "npm ci\nnpm run build"
    assert blocks[0]["heading"] == "Build"
    assert blocks[0]["line"] == 3


def test_secret_assignments_and_remote_shell_recipes_are_not_republished():
    source = "# Installation\n```sh\nTOKEN=secret\npython app.py\n```\n```sh\ncurl https://example.com/a | bash\n```"
    assert docs.install_blocks("README.md", source) == []


@pytest.mark.parametrize(
    "path",
    [
        ".env",
        ".env.py",
        "vendor/a.py",
        "node_modules/a.js",
        "../a.py",
        "/a.py",
        "a.min.js",
        "images/readme.png",
    ],
)
def test_excluded_sources(path):
    assert not docs.source_candidate({"path": path, "type": "blob", "mode": "100644"})


def test_symlinks_are_not_followed():
    assert not docs.source_candidate(
        {"path": "main.py", "type": "blob", "mode": "120000"}
    )


def test_only_named_safe_manifest_tasks_are_published():
    value = docs.manifest_info(
        "package.json",
        '{"scripts":{"build":"next build","postinstall":"unsafe","dev":"TOKEN=secret next dev"}}',
    )
    assert value["scripts"] == [{"name": "build", "command": "next build"}]


def test_cached_source_integrity_is_verified(tmp_path, monkeypatch):
    monkeypatch.setattr(docs, "CACHE", tmp_path)
    sha = "0" * 40
    (tmp_path / "blobs").mkdir()
    (tmp_path / "blobs" / sha).write_bytes(b"changed source")
    with pytest.raises(ValueError, match="integrity"):
        docs.fetch_blob("demo", "1" * 40, {"path": "main.py", "sha": sha}, True)


@pytest.mark.parametrize(
    ("linked_path", "directive", "expected"),
    [
        ("main.py", "", "available"),
        ("removed.py", "", "needs_review"),
        ("main.py", '%%{init: {"securityLevel":"loose"}}%%\n', "needs_review"),
    ],
)
def test_gitdiagram_import_checks_paths_and_never_requests_video(
    tmp_path, monkeypatch, linked_path, directive, expected
):
    monkeypatch.setattr(docs, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(docs, "EXPORT", tmp_path / "exports")
    calls = []
    source = (
        directive + 'flowchart TD\nA["Entry"] --> B["Result"]\n'
        f'click A "https://github.com/antoinebou12/demo/blob/main/{linked_path}"\n'
    )

    def stored_diagram(name, repo):
        calls.append((name, repo))
        return {
            "_meta": {
                "com.gitdiagram/diagram": {
                    "repository": "antoinebou12/demo",
                    "status": "found",
                    "mermaid": source,
                }
            }
        }

    monkeypatch.setattr(docs, "mcp", stored_diagram)
    result = docs.import_gitdiagram("demo", "demo", {"main.py"}, False)
    assert result["status"] == expected
    assert calls == [("get_repository_diagram", "demo")]
    assert (tmp_path / "exports/demo/gitdiagram.mmd").read_text(
        encoding="utf-8"
    ) == source
    if directive:
        assert result["mermaid"] is None
    else:
        assert "click " not in result["mermaid"]
