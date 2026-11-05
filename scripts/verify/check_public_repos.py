"""Fail when the built site links a GitHub repository that is not publicly readable.

Every github.com/<owner>/<repo> link for the site's owners is checked with an anonymous
`git ls-remote` (credential helpers disabled), so a private repository fails even on a
machine that is signed in to GitHub. Usage:

    python scripts/verify/check_public_repos.py [--site docs]
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OWNERS = ("antoinebou12", "AlgoETS", "ETSim")
LINK = re.compile(r"github\.com/(" + "|".join(OWNERS) + r")/([A-Za-z0-9._-]+)")
# GitHub paths under an owner that are not repositories.
NOT_REPOS = {"followers", "following", "repositories", "stars", "sponsors", "orgs", "projects"}
SKIP_DIRS = {"development", "deployment", "infrastructure", "setup", "superpowers", "ux-review"}


def repositories(site):
    found = {}
    for path in site.rglob("*"):
        if path.suffix not in {".html", ".md", ".json", ".xml", ".txt"} or not path.is_file():
            continue
        if path.relative_to(site).parts[0] in SKIP_DIRS:
            continue
        for owner, name in LINK.findall(path.read_text(encoding="utf-8", errors="ignore")):
            name = name.removesuffix(".git").rstrip(".")
            if name and name not in NOT_REPOS:
                found.setdefault(f"{owner}/{name}".lower(), (f"{owner}/{name}", path))
    return found


def is_public(full_name):
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": "echo"}
    result = subprocess.run(
        ["git", "-c", "credential.helper=", "ls-remote", "--exit-code", "-q",
         f"https://github.com/{full_name}.git", "HEAD"],
        env=env, capture_output=True, text=True, timeout=60)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--site", default=str(ROOT / "docs"))
    args = parser.parse_args()
    found = repositories(Path(args.site))
    if not is_public("antoinebou12/CV"):
        print("Warning: GitHub is unreachable; repository visibility was not checked.")
        return 0
    with ThreadPoolExecutor(max_workers=12) as pool:
        results = dict(zip(found, pool.map(lambda key: is_public(found[key][0]), found)))
    private = sorted(key for key, ok in results.items() if not ok)
    for key in private:
        name, path = found[key]
        print(f"Not public: github.com/{name} (linked from {path})")
    print(f"Checked {len(found)} linked repositories; {len(private)} not publicly readable.")
    return 1 if private else 0


if __name__ == "__main__":
    sys.exit(main())
