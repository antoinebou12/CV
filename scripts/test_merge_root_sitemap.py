#!/usr/bin/env python3
"""Tests for scripts/merge_root_sitemap.py (Hugo sitemapindex flattening)."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
SCRIPT = Path(__file__).resolve().parent / "merge_root_sitemap.py"


def q(tag: str) -> str:
    return f"{{{NS}}}{tag}"


class MergeRootSitemapTests(unittest.TestCase):
    def test_flattens_sitemapindex_and_adds_static_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blog = root / "blog"
            en_dir = blog / "en"
            en_dir.mkdir(parents=True)
            urlset = ET.Element(q("urlset"), {"xmlns": NS})
            url = ET.SubElement(urlset, q("url"))
            ET.SubElement(url, q("loc")).text = "https://example.com/CV/blog/en/posts/a/"
            ET.ElementTree(urlset).write(
                en_dir / "sitemap.xml", encoding="utf-8", xml_declaration=True
            )

            index = ET.Element(q("sitemapindex"), {"xmlns": NS})
            sm = ET.SubElement(index, q("sitemap"))
            ET.SubElement(sm, q("loc")).text = "https://example.com/CV/blog/en/sitemap.xml"
            ET.ElementTree(index).write(
                root / "sitemap.xml", encoding="utf-8", xml_declaration=True
            )

            out = root / "out.xml"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(root / "sitemap.xml"),
                    "--output",
                    str(out),
                    "--blog-dir",
                    str(blog),
                    "--site-root",
                    "https://example.com/CV",
                    "--lastmod",
                    "2026-05-19",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)

            merged = ET.parse(out).getroot()
            self.assertEqual(merged.tag, q("urlset"))
            locs = {
                el.find(q("loc")).text
                for el in merged.findall(q("url"))
                if el.find(q("loc")) is not None
            }
            self.assertIn("https://example.com/CV/blog/en/posts/a/", locs)
            self.assertIn("https://example.com/CV/index-en.html", locs)

    def test_urlset_passthrough(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blog = root / "blog"
            blog.mkdir()
            urlset = ET.Element(q("urlset"), {"xmlns": NS})
            url = ET.SubElement(urlset, q("url"))
            ET.SubElement(url, q("loc")).text = "https://example.com/CV/blog/page/"
            ET.ElementTree(urlset).write(
                root / "sitemap.xml", encoding="utf-8", xml_declaration=True
            )

            out = root / "out.xml"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(root / "sitemap.xml"),
                    "--output",
                    str(out),
                    "--blog-dir",
                    str(blog),
                    "--site-root",
                    "https://example.com/CV",
                    "--lastmod",
                    "2026-05-19",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
            locs = {
                el.find(q("loc")).text
                for el in ET.parse(out).getroot().findall(q("url"))
                if el.find(q("loc")) is not None
            }
            self.assertIn("https://example.com/CV/blog/page/", locs)
            self.assertIn("https://example.com/CV/index.html", locs)


if __name__ == "__main__":
    unittest.main()
