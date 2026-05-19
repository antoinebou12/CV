# Local smoke test mirroring .github/workflows (deploy + compile gates).
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File scripts\test-pipeline-local.ps1
# Optional: -SkipCompile  (skip Docker CV build; deploy/link checks only)
param(
    [switch]$SkipCompile
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot

function Write-Step($msg) { Write-Host "`n=== $msg ===" -ForegroundColor Cyan }

Write-Step 'Python: install deps + sitemap tests'
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q
python scripts\test_merge_root_sitemap.py
if ($LASTEXITCODE -ne 0) { throw 'test_merge_root_sitemap failed' }

Write-Step 'Node: Hugo theme CSS (deploy.yml)'
Push-Location hugo
npm ci
if ($LASTEXITCODE -ne 0) { throw 'npm ci failed' }
npm run build:css
if ($LASTEXITCODE -ne 0) { throw 'npm run build:css failed' }
Pop-Location

Write-Step 'Deploy artifact: build _site'
$Site = Join-Path $RepoRoot '_site'
if (Test-Path $Site) { Remove-Item -Recurse -Force $Site }
New-Item -ItemType Directory -Path $Site | Out-Null

foreach ($f in @('index.html', 'index-en.html', 'index-fr.html', '404.html')) {
    if (Test-Path $f) { Copy-Item $f $Site }
}
Get-ChildItem -Path $RepoRoot -File -Include *.png, *.jpg, *.jpeg, *.ico, *.webmanifest, *.xml |
    ForEach-Object { Copy-Item $_.FullName $Site }
if (Test-Path 'antoine.jpeg') { Copy-Item 'antoine.jpeg' $Site }
foreach ($d in @('css', 'linktree', 'papers')) {
    if (Test-Path $d) { Copy-Item -Recurse $d (Join-Path $Site $d) }
}

$Repo = 'CV'
foreach ($pdf in @('cv-en\resume.pdf', 'cv-fr\resume.pdf')) {
    if (-not (Test-Path $pdf)) { throw "Missing $pdf (run compile-cv or build locally first)" }
}
New-Item -ItemType Directory -Path (Join-Path $Site 'cv-en'), (Join-Path $Site 'cv-fr') -Force | Out-Null
Copy-Item 'cv-en\resume.pdf' (Join-Path $Site 'cv-en\resume.pdf') -Force
Copy-Item 'cv-fr\resume.pdf' (Join-Path $Site 'cv-fr\resume.pdf') -Force

$HugoBase = "https://antoineboucher.info/$Repo/blog/"
$env:HUGO_ENV = 'production'
hugo --gc --minify -s hugo -d (Join-Path $Site 'blog') -b $HugoBase
if ($LASTEXITCODE -ne 0) { throw 'hugo build failed' }
if (Test-Path 'favicon.ico') {
    Copy-Item 'favicon.ico' (Join-Path $Site 'blog\favicon.ico') -Force
}

# Promote agent-ready assets (deploy.yml)
New-Item -ItemType Directory -Path (Join-Path $Site '.well-known') -Force | Out-Null
$blog = Join-Path $Site 'blog'
foreach ($pair in @(
        @('robots.txt', 'robots.txt'),
        @('sitemap.xml', 'sitemap.xml'),
        @('llms.txt', 'llms.txt')
    )) {
    $src = Join-Path $blog $pair[0]
    if (Test-Path $src) { Copy-Item $src (Join-Path $Site $pair[1]) -Force }
}
$bkWellKnown = Join-Path $blog '.well-known'
if (Test-Path $bkWellKnown) {
    Copy-Item -Recurse (Join-Path $bkWellKnown '*') (Join-Path $Site '.well-known') -Force
}
if (Test-Path 'hugo\static\_headers') {
    Copy-Item 'hugo\static\_headers' (Join-Path $Site '_headers') -Force
}

function Replace-InFile($path, $pattern, $replacement) {
    if (-not (Test-Path $path)) { return }
    $c = Get-Content -Raw -LiteralPath $path
  $c = $c -replace $pattern, $replacement
    Set-Content -LiteralPath $path -Value $c -NoNewline
}

$from = 'https://antoineboucher.info/blog/'
$to = "https://antoineboucher.info/$Repo/blog/"
foreach ($rel in @(
        '.well-known\api-catalog',
        '.well-known\agent-skills\index.json',
        '.well-known\markdown-map.json',
        '_headers',
        'robots.txt',
        'llms.txt'
    )) {
    Replace-InFile (Join-Path $Site $rel) ([regex]::Escape($from)) $to
}
$mm = Join-Path $Site '.well-known\markdown-map.json'
Replace-InFile $mm '"/blog/agent/home.md"' ('"/' + $Repo + '/blog/agent/home.md"')
Get-ChildItem -Path (Join-Path $Site '.well-known') -Recurse -File -Filter '*.md' -ErrorAction SilentlyContinue |
    ForEach-Object { Replace-InFile $_.FullName ([regex]::Escape($from)) $to }
$agentDir = Join-Path $Site 'blog\agent'
if (Test-Path $agentDir) {
    Get-ChildItem -Path $agentDir -Recurse -File -Filter '*.md' |
        ForEach-Object { Replace-InFile $_.FullName ([regex]::Escape($from)) $to }
}

if (-not (Test-Path (Join-Path $Site 'sitemap.xml'))) {
    throw 'Missing _site/sitemap.xml after promote'
}
$lastmod = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd')
python scripts\merge_root_sitemap.py `
    --input (Join-Path $Site 'sitemap.xml') `
    --output (Join-Path $Site 'sitemap.xml') `
    --blog-dir (Join-Path $Site 'blog') `
    --site-root "https://antoineboucher.info/$Repo" `
    --lastmod $lastmod
if ($LASTEXITCODE -ne 0) { throw 'merge_root_sitemap failed' }
$robots = Join-Path $Site 'robots.txt'
if (Test-Path $robots) {
    $sitemapUrl = "https://antoineboucher.info/$Repo/sitemap.xml"
    (Get-Content -Raw $robots) -replace '(?m)^Sitemap:.*', "Sitemap: $sitemapUrl" |
        Set-Content -LiteralPath $robots -NoNewline
}

Write-Step 'verify_deploy_build.py'
python scripts\verify_deploy_build.py --site-dir $Site --repo $Repo --repo-root $RepoRoot
if ($LASTEXITCODE -ne 0) { throw 'verify_deploy_build failed' }

if (-not $SkipCompile) {
    Write-Step 'Compile CV: Docker + build_cv.py (compile-cv.yml)'
    $env:PYTHONIOENCODING = 'utf-8'
    $prevEap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    docker info *>$null
    $dockerOk = $LASTEXITCODE -eq 0
    $ErrorActionPreference = $prevEap
    if (-not $dockerOk) {
        throw 'Docker is not running. Start Docker Desktop, then re-run without -SkipCompile.'
    }
    foreach ($p in @('build_cv.py', 'Dockerfile.cv', 'cv-en', 'cv-fr')) {
        if (-not (Test-Path $p)) { throw "Missing $p" }
    }
    $lychee = Get-Command lychee -ErrorAction SilentlyContinue
    if ($lychee) {
        & lychee --no-progress --max-retries 3 `
            ./cv-en/latex ./cv-fr/latex ./cv-en/resume.tex ./cv-fr/resume.tex `
            ./letters/en/cover-letter.tex ./letters/fr/cover-letter.tex
        if ($LASTEXITCODE -ne 0) { Write-Warning 'lychee reported issues (same as CI would fail if failIfEmpty)' }
    } else {
        Write-Warning 'lychee not in PATH; skipping link-check step (CI uses lychee-action)'
    }
    python build_cv.py --all --rebuild --verbose --ci
    if ($LASTEXITCODE -ne 0) { throw 'build_cv.py failed' }
    foreach ($f in @('cv-en\resume.pdf', 'cv-fr\resume.pdf')) {
        if (-not (Test-Path $f) -or (Get-Item $f).Length -eq 0) { throw "Invalid $f" }
    }
}

Write-Host "`nLocal pipeline smoke test passed." -ForegroundColor Green
