"""Build the local production website into docs without removing documentation."""
import argparse
import os
from datetime import date
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "docs"


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, type=date.fromisoformat,
                        help="Release date in America/Toronto (YYYY-MM-DD)")
    args = parser.parse_args()
    # Stage separately: failed builds never overwrite the published tree.
    with tempfile.TemporaryDirectory(prefix="cv-pages-") as temporary:
        site = Path(temporary)
        for name in ("index.html", "index-en.html", "index-fr.html",
                     "404.html", "resume.md", "resume-fr.md"):
            shutil.copy2(ROOT / name, site / name)
        for language, name in (("en", "resume.json"), ("fr", "resume-fr.json")):
            shutil.copy2(ROOT / f"data/resume.{language}.json", site / name)
            (site / f"cv-{language}").mkdir()
            shutil.copy2(ROOT / f"cv-{language}/resume.pdf", site / f"cv-{language}/resume.pdf")
        for extension in ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.ico", "*.webmanifest"):
            for source in ROOT.glob(extension):
                shutil.copy2(source, site / source.name)
        for name in ("css", "js", "linktree", "papers", "images"):
            shutil.copytree(ROOT / name, site / name)
        os.environ.update(HUGO_ENV="production", HUGO_PARAMS_GITHUBPAGESREPO="CV")
        run("hugo", "--gc", "--minify", "-s", "hugo", "-d", str(site / "blog"),
            "-b", "https://antoineboucher.info/CV/blog/")
        # Never publish thesis PDFs, including ignored files present locally.
        for slug in ("graphquon-2025-university-of-toronto", "thesis-wear-texture-space"):
            for source in (site / "blog").rglob("*.pdf"):
                if slug in source.parts:
                    source.unlink()
        shutil.copy2(ROOT / "favicon.ico", site / "blog/favicon.ico")
        for presentation in site.rglob("*.pptx"):
            if presentation.stat().st_size <= 50_000_000:
                continue
            relative = presentation.relative_to(site).as_posix()
            source = relative.replace("blog/posts/", "hugo/content/posts/", 1)
            download = "https://media.githubusercontent.com/media/antoinebou12/CV/main/" + quote(source)
            for page in site.rglob("*.html"):
                content = page.read_text(encoding="utf-8")
                updated = content.replace("/CV/" + relative, download)
                if updated != content:
                    page.write_text(updated, encoding="utf-8")
            presentation.unlink()
        shutil.copytree(site / "blog/.well-known", site / ".well-known")
        for name in ("robots.txt", "sitemap.xml", "llms.txt", "llms-full.txt"):
            shutil.copy2(site / "blog" / name, site / name)
        if (ROOT / "hugo/static/_headers").exists():
            shutil.copy2(ROOT / "hugo/static/_headers", site / "_headers")
        discovery = list((site / ".well-known").rglob("*"))
        discovery += list((site / "blog/agent").rglob("*.md"))
        discovery += [site / name for name in ("robots.txt", "llms.txt", "_headers")]
        for source in discovery:
            if source.is_file():
                text = source.read_text(encoding="utf-8")
                text = text.replace("https://antoineboucher.info/blog/", "https://antoineboucher.info/CV/blog/")
                text = text.replace('"/blog/agent/home.md"', '"/CV/blog/agent/home.md"')
                source.write_text(text, encoding="utf-8")
        run(sys.executable, "scripts/deploy/merge_root_sitemap.py", "--input", str(site / "sitemap.xml"),
            "--output", str(site / "sitemap.xml"), "--blog-dir", str(site / "blog"),
            "--site-root", "https://antoineboucher.info/CV", "--lastmod", args.date.isoformat())
        robots = site / "robots.txt"
        robots.write_text("\n".join("Sitemap: https://antoineboucher.info/CV/sitemap.xml" if line.startswith("Sitemap:")
                                     else line for line in robots.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
        (site / ".nojekyll").touch()
        run(sys.executable, "scripts/verify/verify_deploy_build.py", "--site-dir", str(site), "--repo-root", str(ROOT))
        run(sys.executable, "scripts/verify/check_sitemap_coverage.py", "--site-dir", str(site))
        removed = prune_generated(site)
        shutil.copytree(site, DEST, dirs_exist_ok=True)
        print(f"Production website built in {DEST}; removed {removed} stale generated files; "
              "existing documentation preserved.")


def prune_generated(site):
    """Delete files under the generated directories (blog/, css/, .well-known/, ...) that this
    build no longer produces, so superseded bundles, renamed pages and deleted images stop
    being served. Directories the build does not create, such as docs/development/, are untouched."""
    removed = 0
    for directory in (path for path in site.iterdir() if path.is_dir()):
        published = DEST / directory.name
        if not published.is_dir():
            continue
        for old in sorted(published.rglob("*"), reverse=True):
            relative = old.relative_to(DEST)
            if old.is_file() and not (site / relative).exists():
                old.unlink()
                removed += 1
            elif old.is_dir() and not any(old.iterdir()):
                old.rmdir()
    return removed


if __name__ == "__main__":
    main()
