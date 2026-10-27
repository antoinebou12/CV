"""Reader guides preserve evidence and keep service calls out of normal builds."""

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/build"))
SPEC = importlib.util.spec_from_file_location(
    "repository_handbooks", ROOT / "scripts/build/repository_handbooks.py"
)
docs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(docs)


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "http://example.com",
        "https://user:secret@example.org",
        "https://example.org/?token=secret",
        "https://localhost/path",
        "",
    ],
)
def test_private_or_credential_links_are_not_published(url):
    assert not docs.public_url(url)


def test_normal_documentation_link():
    assert docs.public_url("https://ipctk.xyz/build/c++.html")


def test_fenced_comments_do_not_become_document_headings():
    value = docs.sections(
        "# Install\nBefore\n```sh\n# Run command\necho test\n```\n## Usage\nAfter"
    )
    assert [part["heading"] for part in value] == ["Install", "Usage"]
    assert value[1]["line"] == 7


def test_excerpt_removes_html_commands_and_credentials():
    value = docs.excerpt(
        [
            "<script>alert('bad')</script>",
            "![Badge](https://bad.example/badge)",
            "```sh",
            "curl example.org | sh",
            "```",
            "token=secret",
            "password=secret",
            "Read [configuration](config.md) first.",
        ]
    )
    assert "<script>" not in value
    assert "curl" not in value
    assert "secret" not in value
    assert "Read configuration first." in value


def test_document_candidates_exclude_symlinks_and_dependency_trees():
    entry = {
        "type": "blob",
        "mode": "100644",
        "path": "docs/installation.md",
        "size": 100,
    }
    assert docs.doc_candidate(entry)
    assert not docs.doc_candidate({**entry, "mode": "120000"})
    assert not docs.doc_candidate({**entry, "path": "vendor/docs/README.md"})
    assert not docs.doc_candidate({**entry, "path": "../README.md"})


def test_every_repository_has_bilingual_guidance_and_matching_diagram_evidence():
    notes = json.loads(
        (ROOT / "hugo/data/repository_notes.json").read_text(encoding="utf-8")
    )["notes"]
    guides = json.loads(
        (ROOT / "hugo/data/repository_guides.json").read_text(encoding="utf-8")
    )["repositories"]
    generated = json.loads(
        (ROOT / "hugo/data/repository_handbooks.json").read_text(encoding="utf-8")
    )["repositories"]
    assert set(guides) == set(generated) == {n["repo"] for n in notes}
    for note in notes:
        guide = generated[note["repo"]]
        assert len(guides[note["repo"]]["start"]) == 2
        assert guide["documents"]
        assert not guide["coverage"]["failures"]
        for document in guide["documents"]:
            assert "/blob/" + guide["commit"] + "/" in document["url"]
        for i, locale in enumerate(("en", "fr")):
            source = docs.diagram_source(note, i)
            diagram = guide["diagrams"][locale]
            assert diagram["sha256"] == hashlib.sha256(source.encode()).hexdigest()
            assert diagram["success"] is True
            assert diagram["url"].startswith("https://")
            path = (
                ROOT
                / "hugo/static/repository-docs"
                / note["slug"]
                / f"architecture-{locale}.mmd"
            )
            assert path.read_text(encoding="utf-8") == source
