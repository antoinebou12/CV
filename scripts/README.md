# Scripts

| Folder | Purpose |
|--------|---------|
| `build/` | Generate LaTeX, HTML (AEO/About), JSON-LD, Markdown resume from `data/` |
| `html/` | Patch and sync static CV HTML; extract CSS |
| `deploy/` | Sitemap merge, image optimization |
| `verify/` | Schema, EN/FR parity, deploy and meta checks |
| `hugo/` | Hugo tag merge helper |
| `ci/` | Local smoke test (`test-pipeline-local.ps1`), `act`, aggregated tests |
| `tests/` | Python unit tests |

Repo root is resolved via `scripts/_repo.py` (`REPO_ROOT`).

## Common commands

```powershell
# Quality + unit tests (no Docker)
pwsh -File scripts/ci/run-tests.ps1

# Full local smoke (mirrors deploy + optional compile)
pwsh -File scripts/ci/test-pipeline-local.ps1 -SkipCompile

# GitHub Actions locally (quality workflow)
pwsh -File scripts/ci/run-act.ps1
```

```bash
python scripts/build/generate_cv.py
python scripts/build/generate_aeo_content.py --all
python scripts/html/sync_index_html.py
```
