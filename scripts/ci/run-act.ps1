# Run quality workflow locally with act (https://github.com/nektos/act).
# Usage: pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/ci/run-act.ps1
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $RepoRoot

$act = Get-Command act -ErrorAction SilentlyContinue
if (-not $act) {
    throw 'act is not on PATH. Install: https://github.com/nektos/act#installation'
}

# en-fr-parity matches relocated scripts; spellcheck flags French copy by design.
& act push -W .github/workflows/quality.yml -j en-fr-parity --container-architecture linux/amd64
if ($LASTEXITCODE -ne 0) { throw 'act en-fr-parity job failed' }

Write-Host "`nact en-fr-parity job finished." -ForegroundColor Green
