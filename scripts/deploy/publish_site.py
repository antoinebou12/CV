"""Build the CV and blog locally; optionally commit docs and push to main."""
import argparse
import os
import re
from datetime import datetime
from pathlib import Path
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]


def run(*args, cwd=ROOT, capture=False):
    return subprocess.run(args, cwd=cwd, check=True, text=True,
                          stdout=subprocess.PIPE if capture else None).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true",
                        help="Commit generated docs and push HEAD to origin/main")
    parser.add_argument("--date", default=datetime.now(ZoneInfo("America/Toronto")).date().isoformat())
    args = parser.parse_args()
    git = str(Path("C:/Program Files/Git/cmd/git.exe")) if sys.platform == "win32" else "git"
    if not shutil.which("hugo"):
        parser.error("Install Hugo extended before building.")
    theme = ROOT / "hugo/themes/paper"
    if not theme.is_dir() or not any(theme.iterdir()):
        # Without the theme, Hugo fails later with an unrelated-looking resources.Concat error.
        parser.error("The Paper theme submodule is missing: run "
                     "'git submodule update --init hugo/themes/paper'.")
    expected = re.search(r'hugo-version:\s*"([^"]+)"',
                         (ROOT / ".github/workflows/quality.yml").read_text(encoding="utf-8"))
    installed = run("hugo", "version", capture=True)
    if expected and f"v{expected[1]}" not in installed:
        print(f"Warning: CI builds with Hugo {expected[1]}; local {installed.split()[0]} may render differently.")
    if args.publish:
        if run(git, "status", "--porcelain", "--untracked-files=no", capture=True).strip():
            parser.error("Commit tracked source changes before publishing.")
        run(git, "fetch", "origin", "main")
        run(git, "merge-base", "--is-ancestor", "origin/main", "HEAD")
    # Publish with the checked-in theme CSS expected by our template overrides.
    run(sys.executable, "scripts/build/article_sources.py")
    run(sys.executable, "scripts/deploy/build_docs.py", "--date", args.date)
    # Never publish a link to a repository that is not public.
    run(sys.executable, "scripts/verify/check_public_repos.py", "--site", str(ROOT / "docs"))
    if shutil.which("node"):
        # The same project-note checks CI runs, against the output about to be published.
        subprocess.run(["node", "--test", "scripts/verify/repository-notes.test.mjs"], cwd=ROOT, check=True,
                       env={**os.environ, "CV_NOTES_SITE": str(ROOT / "docs/blog")})
    else:
        print("Warning: Node.js not found; skipped scripts/verify/repository-notes.test.mjs.")
    if args.publish:
        run(git, "add", "--", "docs")
        changed = run(git, "diff", "--cached", "--name-only", capture=True).strip()
        if changed:
            run(git, "commit", "-m", f"Publish CV and blog ({args.date})")
        run(git, "push", "origin", "HEAD:main")
        print("Pushed docs to main. GitHub Pages must finish processing before the site is live.")
    else:
        print("Review docs locally. Use --publish from a clean source checkout to publish.")


if __name__ == "__main__":
    main()
