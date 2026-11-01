param(
    [ValidateSet('Chrome', 'Edge')][string]$Browser = 'Chrome',
    [ValidateRange(1024, 65535)][int]$Port = 8934,
    [switch]$Build
)
$ErrorActionPreference = 'Stop'
$siteRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
if ($Build) {
    Push-Location $siteRoot
    try {
        & uv run --no-project --python 3.14 --with tzdata python scripts/deploy/publish_site.py
        if ($LASTEXITCODE -ne 0) { throw 'The local site build failed.' }
    } finally { Pop-Location }
}
$siteUrl = "http://127.0.0.1:$Port/CV/"
try { $null = Invoke-WebRequest -Uri "${siteUrl}index-en.html" -TimeoutSec 2 -UseBasicParsing }
catch {
    $uvPath = (Get-Command uv -ErrorAction Stop).Source
    $serverScript = Join-Path $PSScriptRoot 'serve_webmcp.py'
    Start-Process -FilePath $uvPath -ArgumentList @('run', '--no-project', '--python', '3.14', 'python', ('"{0}"' -f $serverScript), '--port', $Port) -WorkingDirectory $siteRoot -WindowStyle Hidden
    $serverReady = $false
    for ($attempt = 0; $attempt -lt 40; $attempt++) {
        Start-Sleep -Milliseconds 250
        try { $null = Invoke-WebRequest -Uri "${siteUrl}index-en.html" -TimeoutSec 1 -UseBasicParsing; $serverReady = $true; break } catch { }
    }
    if (-not $serverReady) { throw "The preview server did not start on port $Port." }
}
$browserExe = if ($Browser -eq 'Chrome') { Join-Path $env:ProgramFiles 'Google/Chrome/Application/chrome.exe' } else { Join-Path ${env:ProgramFiles(x86)} 'Microsoft/Edge/Application/msedge.exe' }
if (-not (Test-Path -LiteralPath $browserExe)) { throw "$Browser is not installed at $browserExe" }
$profilePath = Join-Path $env:LOCALAPPDATA "CV-WebMCP/$Browser"
Start-Process -FilePath $browserExe -ArgumentList @(
    ('--user-data-dir="{0}"' -f $profilePath),
    '--enable-features=WebMCP', '--enable-blink-features=WebMCP', '--no-first-run',
    "${siteUrl}index-en.html", "${siteUrl}blog/posts/ipc-toolkit-contact-library/"
)
Write-Output "Opened WebMCP-enabled $Browser for the CV and Hugo. Profile: $profilePath"
