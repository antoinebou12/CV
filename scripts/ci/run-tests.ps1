# Fast local tests (unit + quality gates, no Hugo deploy / Docker).
# Usage: pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/ci/run-tests.ps1
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $RepoRoot

python -m pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install -r requirements-ci.txt -q

python scripts/tests/test_merge_root_sitemap.py
if ($LASTEXITCODE -ne 0) { throw 'test_merge_root_sitemap failed' }

python scripts/tests/test_render_resume_md.py
if ($LASTEXITCODE -ne 0) { throw 'test_render_resume_md failed' }

python scripts/tests/test_generate_aeo_content.py
if ($LASTEXITCODE -ne 0) { throw 'test_generate_aeo_content failed' }

python scripts/build/generate_cv.py --check
if ($LASTEXITCODE -ne 0) { throw 'generate_cv --check failed (run: python scripts/build/generate_cv.py, then commit skills.tex)' }

python scripts/verify/validate_cv_data.py
if ($LASTEXITCODE -ne 0) { throw 'validate_cv_data failed' }

python scripts/verify/check_en_fr_parity.py
if ($LASTEXITCODE -ne 0) { throw 'check_en_fr_parity failed' }

Write-Host "`nAll local tests passed." -ForegroundColor Green
