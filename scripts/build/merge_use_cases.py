"""Merge per-repository use-case files into hugo/data/project_use_cases.json and validate them.

Each input file is one repository (see the schema in docs/development/project-use-cases.md).
Usage: python scripts/build/merge_use_cases.py <dir with RepoName.json files> [--check]
--check only validates the existing data file.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "hugo/data/project_use_cases.json"
LIMITS = {"summary": 140, "actor": 24, "case": 32}


def pair(value, where, limit=None):
    errors = []
    if not (isinstance(value, list) and len(value) == 2 and all(isinstance(v, str) and v.strip() for v in value)):
        return [f"{where}: expected [English, French]"]
    if limit:
        errors += [f"{where}: '{v}' is longer than {limit} characters" for v in value if len(v) > limit]
    return errors


def validate(name, data):
    errors = pair(data.get("summary"), f"{name}.summary", LIMITS["summary"])
    actors = data.get("actors") or []
    ids = {a.get("id") for a in actors}
    if not 1 <= len(actors) <= 3:
        errors.append(f"{name}: 1 to 3 actors expected, found {len(actors)}")
    for actor in actors:
        if actor.get("kind") not in {"person", "system"}:
            errors.append(f"{name}.{actor.get('id')}: kind must be person or system")
        errors += pair(actor.get("label"), f"{name}.{actor.get('id')}.label", LIMITS["actor"])
    cases = data.get("use_cases") or []
    if not 3 <= len(cases) <= 6:
        errors.append(f"{name}: 3 to 6 use cases expected, found {len(cases)}")
    used = set()
    for case in cases:
        errors += pair(case.get("label"), f"{name}.{case.get('id')}.label", LIMITS["case"])
        if case.get("detail") is not None:
            errors += pair(case.get("detail"), f"{name}.{case.get('id')}.detail")
        unknown = set(case.get("actors") or []) - ids
        if not case.get("actors") or unknown:
            errors.append(f"{name}.{case.get('id')}: actors missing or unknown {sorted(unknown)}")
        used |= set(case.get("actors") or [])
    if ids - used:
        errors.append(f"{name}: actors without a use case {sorted(ids - used)}")
    scenario = data.get("scenario") or {}
    errors += pair(scenario.get("title"), f"{name}.scenario.title")
    steps = scenario.get("steps") or []
    if not 3 <= len(steps) <= 6:
        errors.append(f"{name}: 3 to 6 scenario steps expected, found {len(steps)}")
    for k, step in enumerate(steps):
        errors += pair(step, f"{name}.scenario.steps[{k}]")
    if not data.get("evidence"):
        errors.append(f"{name}: evidence is empty")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", nargs="?")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads(TARGET.read_text(encoding="utf-8")) if TARGET.exists() else {"repositories": {}}
    if not args.check:
        for path in sorted(Path(args.source).glob("*.json")):
            if path.name.endswith(".meta.json"):
                continue
            entry = json.loads(path.read_text(encoding="utf-8"))
            data["repositories"][entry.get("repo") or path.stem] = entry
        data["repositories"] = dict(sorted(data["repositories"].items(), key=lambda kv: kv[0].lower()))
        TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    errors = [e for name, entry in data["repositories"].items() for e in validate(name, entry)]
    for error in errors:
        print(error)
    print(f"{len(data['repositories'])} repositories; {len(errors)} problems.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
