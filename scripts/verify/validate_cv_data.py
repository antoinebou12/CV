"""Validate data/cv.yaml against data/cv.schema.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import sys

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT as ROOT
DATA = ROOT / "data" / "cv.yaml"
SCHEMA = ROOT / "data" / "cv.schema.json"


def main() -> int:
    try:
        import yaml
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        print(f"Missing dependency: {exc}. pip install -r requirements-ci.txt")
        return 1

    if not DATA.is_file():
        print(f"Missing {DATA.relative_to(ROOT)}")
        return 1

    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        print("cv.yaml validation FAILED:")
        for err in errors:
            path = ".".join(str(p) for p in err.path) or "(root)"
            print(f"  {path}: {err.message}")
        return 1

    skill_ids = {s["id"] for s in data.get("skills", [])}
    for profile, groups in data.get("skill_groups", {}).items():
        for group in groups:
            if not group.get("latex_line") and not group.get("generated"):
                if not group.get("skill_ids"):
                    print(
                        f"Group {group.get('category')!r} in skill_groups.{profile} "
                        "needs skill_ids, latex_line, or generated"
                    )
                    return 1
            for sid in group.get("skill_ids", []) + group.get("intermediate_ids", []):
                if sid not in skill_ids:
                    print(f"Unknown skill id {sid!r} in skill_groups.{profile}")
                    return 1

    print("cv.yaml validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
