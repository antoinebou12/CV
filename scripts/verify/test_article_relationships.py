"""Regression checks for incidental diagram credits in related-project links."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "build/repository_docs.py"
SPEC = importlib.util.spec_from_file_location("repository_docs", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ArticleRelationships(unittest.TestCase):
    def test_diagram_credit_is_not_article_subject(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            content = root / "hugo/content/posts"
            content.mkdir(parents=True)
            fixtures = {
                "printing.md": 'title: "Printing figures"\nRendered with https://github.com/antoinebou12/uml-mcp',
                "diagrams.md": 'title: "uml-mcp from chat"\nhttps://github.com/antoinebou12/uml-mcp',
                "diagrams.fr.md": 'title: "uml-mcp depuis le chat"\nhttps://github.com/antoinebou12/uml-mcp',
                "homebrew.md": 'title: "Homebrew"\nhttps://github.com/antoinebou12/moonlight-n3ds',
                "subject.md": 'title: "A workspace"\nproject_docs: artemis-n3ds\nhttps://github.com/antoinebou12/uml-mcp',
            }
            for name, text in fixtures.items():
                (content / name).write_text(text, encoding="utf-8")
            with patch.object(MODULE, "ROOT", root):
                index = MODULE.repo_articles([{"repo": "uml-mcp", "slug": "uml-mcp"},
                                              {"repo": "Artemis-N3DS", "slug": "artemis-n3ds"}])
            self.assertEqual([item["path"] for item in index["repositories"]["uml-mcp"]],
                             ["posts/diagrams.fr.md", "posts/diagrams.md"])
            self.assertEqual(index["repositories"]["Artemis-N3DS"][0]["path"], "posts/homebrew.md")
            self.assertEqual(index["repositories"]["Artemis-N3DS"][1]["path"], "posts/subject.md")


if __name__ == "__main__":
    unittest.main()
