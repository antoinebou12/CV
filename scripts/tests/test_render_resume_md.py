#!/usr/bin/env python3
"""Tests for scripts/build/render_resume_md.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(__file__).resolve().parents[1] / "build" / "render_resume_md.py"
DATA_EN = REPO_ROOT / "data" / "resume.en.json"


class RenderResumeMdTests(unittest.TestCase):
    def test_render_en_contains_required_headings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data_dir = root / "data"
            data_dir.mkdir()
            out = root / "resume.md"
            payload = json.loads(DATA_EN.read_text(encoding="utf-8"))
            (data_dir / "resume.en.json").write_text(
                json.dumps(payload), encoding="utf-8"
            )
            # Patch module paths by running script against copied data
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--locale", "en"],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
            rendered = (REPO_ROOT / "resume.md").read_text(
                encoding="utf-8"
            )
            for heading in (
                "# Antoine Boucher",
                "## Contact",
                "## Summary",
                "## Experience",
                "## Education",
                "## Skills",
                "## Selected projects",
            ):
                self.assertIn(heading, rendered)

    def test_all_locales_exit_zero(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--all"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)


if __name__ == "__main__":
    unittest.main()
