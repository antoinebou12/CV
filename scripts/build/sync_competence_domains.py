"""Sync data/competence_domains.yaml → hugo/data/competence_domains.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

_BUILD = Path(__file__).resolve().parent
_SCRIPTS = _BUILD.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT

SRC = REPO_ROOT / "data" / "competence_domains.yaml"
DST = REPO_ROOT / "hugo" / "data" / "competence_domains.json"


def render() -> str:
    data = yaml.safe_load(SRC.read_text(encoding="utf-8"))
    out = {
        "majors": [
            {
                "id": m["id"],
                "label": [m["label"]["en"], m["label"]["fr"]],
                "subs": [
                    {
                        "id": s["id"],
                        "label": [s["label"]["en"], s["label"]["fr"]],
                    }
                    for s in m.get("subs", [])
                ],
            }
            for m in data["majors"]
        ],
        "repositories": data.get("repositories", {}),
    }
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if Hugo JSON is out of date",
    )
    args = parser.parse_args()
    text = render()
    if args.check:
        if not DST.is_file() or DST.read_text(encoding="utf-8") != text:
            print("sync_competence_domains.py --check FAILED. Run:")
            print("  python scripts/build/sync_competence_domains.py")
            return 1
        print("sync_competence_domains.py --check passed.")
        return 0
    DST.write_text(text, encoding="utf-8")
    print(f"Wrote {DST.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
