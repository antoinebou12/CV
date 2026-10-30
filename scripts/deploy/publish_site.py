"""Build the CV and blog locally; optionally commit docs and push to main."""
import argparse
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
    if args.publish:
        if run(git, "status", "--porcelain", "--untracked-files=no", capture=True).strip():
            parser.error("Commit tracked source changes before publishing.")
        run(git, "fetch", "origin", "main")
        run(git, "merge-base", "--is-ancestor", "origin/main", "HEAD")
    # Publish with the checked-in theme CSS expected by our template overrides.
    run(sys.executable, "scripts/deploy/build_docs.py", "--date", args.date)
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
