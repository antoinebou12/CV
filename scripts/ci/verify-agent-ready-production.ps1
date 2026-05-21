# Spot-check public URLs for Agent-Ready style artifacts (run after deploy + cache purge).
# Usage: pwsh -File scripts/ci/verify-agent-ready-production.ps1 [-BaseUrl https://antoineboucher.info] [-SitePrefix /CV]
# Use -SitePrefix /CV when the GitHub Pages project is served under that path on the custom domain.

param(
    [string] $BaseUrl = 'https://antoineboucher.info',
    [string] $SitePrefix = ''
)

$ErrorActionPreference = 'Stop'
$u = $BaseUrl.TrimEnd('/')
$prefix = if ([string]::IsNullOrWhiteSpace($SitePrefix)) { '' } else { $SitePrefix.TrimEnd('/') }

function Join-Prefix([string] $Path) {
    $p = $Path.TrimStart('/')
    if ($prefix) {
        return "$prefix/$p"
    }
    return "/$p"
}

function Test-Get {
    param([string] $Path, [string[]] $BodyMustContain = @())
    $url = "$u$Path"
    try {
        $r = Invoke-WebRequest -Uri $url -Method Get -UseBasicParsing -TimeoutSec 30
    } catch {
        Write-Host "FAIL $Path $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    if ($r.StatusCode -lt 200 -or $r.StatusCode -ge 300) {
        Write-Host "FAIL $Path status=$($r.StatusCode)" -ForegroundColor Red
        return $false
    }
    $ct = $r.Headers['Content-Type']
    $body = [string]$r.Content
    foreach ($needle in $BodyMustContain) {
        if (-not $body.Contains($needle)) {
            Write-Host "FAIL $Path body missing: $needle" -ForegroundColor Red
            return $false
        }
    }
    Write-Host "OK   $Path ($ct)" -ForegroundColor Green
    return $true
}

$ok = $true
$ok = (Test-Get (Join-Prefix '/robots.txt') -BodyMustContain @('User-agent:', 'Sitemap:')) -and $ok
$ok = (Test-Get (Join-Prefix '/.well-known/api-catalog') -BodyMustContain @('"linkset"')) -and $ok
$ok = (Test-Get (Join-Prefix '/.well-known/agent-skills/index.json') -BodyMustContain @('"$schema"', '"skills"')) -and $ok
$ok = (Test-Get (Join-Prefix '/sitemap.xml') -BodyMustContain @('<urlset', '<loc>', 'index-en.html')) -and $ok
$ok = (Test-Get (Join-Prefix '/resume.md') -BodyMustContain @('# Antoine Boucher', '## Experience')) -and $ok
$ok = (Test-Get (Join-Prefix '/resume.json') -BodyMustContain @('"basics"', '"work"')) -and $ok
$ok = (Test-Get (Join-Prefix '/llms.txt') -BodyMustContain @('resume.md', 'resume.json')) -and $ok

if (-not $ok) { exit 1 }
Write-Host 'All checks passed.' -ForegroundColor Green
exit 0
