#Requires -Version 5.1
<#
  Applies scripts/tag-merge-map.json to Hugo content front matter (tags: lists).
  Map format: { "OldTag": "CanonicalTag" } — keys and values are exact YAML tag strings.
  Run from repo root: pwsh -File scripts/Apply-TagMerge.ps1
  Uses UTF-8 (no BOM) when rewriting files.
#>
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path -LiteralPath (Join-Path $root 'hugo\hugo.toml'))) {
    throw "Could not find hugo\hugo.toml from $root (run from CV repo root)."
}
$mapPath = Join-Path $PSScriptRoot 'tag-merge-map.json'
$hugoContent = Join-Path $root 'hugo\content'
if (-not (Test-Path -LiteralPath $mapPath)) { throw "Missing $mapPath" }
if (-not (Test-Path -LiteralPath $hugoContent)) { throw "Missing $hugoContent" }

$map = Get-Content -LiteralPath $mapPath -Raw | ConvertFrom-Json
$pairs = @($map.PSObject.Properties)
if ($pairs.Count -eq 0) {
    Write-Host 'tag-merge-map.json is empty - no tag rewrites.'
    exit 0
}

$oldToNew = @{}
foreach ($p in $pairs) {
    $oldToNew[$p.Name] = [string]$p.Value
}

function Rewrite-TagsLine {
    param([string]$line, [hashtable]$map)
    $m = [regex]::Match($line, '^\s*-\s*(.+)\s*$')
    if (-not $m.Success) { return $line, $false }
    $val = $m.Groups[1].Value.Trim().Trim('"').Trim("'")
    if ($map.ContainsKey($val)) {
        $newVal = $map[$val]
        $indent = $line -replace '^(\s*).*', '$1'
        return ($indent + '- ' + $newVal), $true
    }
    return $line, $false
}

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$changedFiles = 0
Get-ChildItem -LiteralPath $hugoContent -Recurse -Filter '*.md' | ForEach-Object {
    $path = $_.FullName
    $raw = [System.IO.File]::ReadAllText($path)
    if ($raw -notmatch '(?s)\A---\r?\n.*?\r?\n---\r?\n') { return }
    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.AddRange([string[]][System.IO.File]::ReadAllLines($path))
    $inFm = $false
    $inTags = $false
    $fileChanged = $false
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($i -eq 0 -and $line -eq '---') { $inFm = $true; continue }
        if ($inFm -and $line -eq '---') { $inFm = $false; $inTags = $false; continue }
        if (-not $inFm) { continue }
        if ($line -match '^tags:\s*$') { $inTags = $true; continue }
        if ($inTags -and ($line -match '^\s+-\s')) {
            $newLine, $ch = Rewrite-TagsLine $line $oldToNew
            if ($ch) { $lines[$i] = $newLine; $fileChanged = $true }
            continue
        }
        if ($inTags -and ($line -match '^\S') -and ($line -notmatch '^\s+-\s')) {
            $inTags = $false
        }
    }
    if ($fileChanged) {
        $out = ($lines -join [Environment]::NewLine)
        if (-not $raw.EndsWith("`n")) { $out = $out.TrimEnd("`r", "`n") + "`n" }
        [System.IO.File]::WriteAllText($path, $out, $utf8NoBom)
        $changedFiles++
        Write-Host "Updated: $path"
    }
}

Write-Host "Done. Files changed: $changedFiles"
