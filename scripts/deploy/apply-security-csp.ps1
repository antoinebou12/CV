<#
.SYNOPSIS
  Apply (or dry-run) the Content-Security-Policy Transform Rule for antoineboucher.info.

.DESCRIPTION
  Reads the CSP value from hugo/static/_headers and upserts a zone Response Header
  Transform Rule (ref: security_csp). Requires Zone Transform Rules Write.

.PARAMETER ZoneId
  Cloudflare zone ID for antoineboucher.info. Optional if CLOUDFLARE_ZONE_ID is set;
  otherwise resolved via the API from -ZoneName.

.PARAMETER ZoneName
  Defaults to antoineboucher.info.

.PARAMETER DryRun
  Print the planned rule payload without calling the Cloudflare API.

.EXAMPLE
  $env:CLOUDFLARE_API_TOKEN = '...'
  .\scripts\deploy\apply-security-csp.ps1

.EXAMPLE
  .\scripts\deploy\apply-security-csp.ps1 -DryRun
#>
[CmdletBinding()]
param(
  [string]$ZoneId = $env:CLOUDFLARE_ZONE_ID,
  [string]$ZoneName = "antoineboucher.info",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$HeadersFile = Join-Path $RepoRoot "hugo\static\_headers"
$Token = $env:CLOUDFLARE_API_TOKEN
if (-not $Token -and -not $DryRun) {
  throw "Set CLOUDFLARE_API_TOKEN (Zone Transform Rules Write) or pass -DryRun."
}

$cspLine = Get-Content $HeadersFile | Where-Object { $_ -match '^\s*Content-Security-Policy:\s*(.+)$' } | Select-Object -First 1
if (-not $cspLine) { throw "No Content-Security-Policy line in $HeadersFile" }
$csp = ($cspLine -replace '^\s*Content-Security-Policy:\s*', '').Trim()

function Invoke-CfApi {
  param([string]$Method, [string]$Path, [object]$Body = $null)
  $uri = "https://api.cloudflare.com/client/v4$Path"
  $headers = @{ Authorization = "Bearer $Token"; "Content-Type" = "application/json" }
  $params = @{ Method = $Method; Uri = $uri; Headers = $headers }
  if ($null -ne $Body) { $params.Body = ($Body | ConvertTo-Json -Depth 20 -Compress) }
  $res = Invoke-RestMethod @params
  if (-not $res.success) { throw ($res.errors | ConvertTo-Json -Depth 5) }
  return $res.result
}

$rule = @{
  ref         = "security_csp"
  description = "SecurityCSP: Content-Security-Policy from hugo/static/_headers"
  expression  = '(http.host eq "' + $ZoneName + '" or http.host eq "www.' + $ZoneName + '")'
  action      = "rewrite"
  enabled     = $true
  action_parameters = @{
    headers = @{
      "Content-Security-Policy" = @{
        operation = "set"
        value     = $csp
      }
      "Cross-Origin-Opener-Policy" = @{
        operation = "set"
        value     = "same-origin-allow-popups"
      }
    }
  }
}

if ($DryRun) {
  Write-Host "Dry run - would upsert rule:"
  $rule | ConvertTo-Json -Depth 10
  Write-Host ("CSP length: {0}" -f $csp.Length)
  exit 0
}

if (-not $ZoneId) {
  $zones = Invoke-CfApi -Method GET -Path ("/zones?name={0}" -f [uri]::EscapeDataString($ZoneName))
  $zone = @($zones) | Select-Object -First 1
  if (-not $zone) { throw ("Zone not found: {0}" -f $ZoneName) }
  $ZoneId = $zone.id
  Write-Host ("Resolved zone {0} -> {1}" -f $ZoneName, $ZoneId)
}

$entrypoint = $null
try {
  $entrypoint = Invoke-CfApi -Method GET -Path "/zones/$ZoneId/rulesets/phases/http_response_headers_transform/entrypoint"
} catch {
  Write-Host "No entrypoint yet; creating zone ruleset for http_response_headers_transform"
  $created = Invoke-CfApi -Method POST -Path "/zones/$ZoneId/rulesets" -Body @{
    name        = "default"
    kind        = "zone"
    phase       = "http_response_headers_transform"
    description = "Response Header Transform Rules"
    rules       = @($rule)
  }
  Write-Host ("Created ruleset {0} with SecurityCSP" -f $created.id)
  exit 0
}

$existing = @($entrypoint.rules)
$kept = @($existing | Where-Object { $_.ref -ne "security_csp" })
$newRules = @($kept + $rule)
$cleanRules = foreach ($r in $newRules) {
  $obj = [ordered]@{
    ref               = $r.ref
    description       = $r.description
    expression        = $r.expression
    action            = $r.action
    enabled           = if ($null -ne $r.enabled) { [bool]$r.enabled } else { $true }
    action_parameters = $r.action_parameters
  }
  if ($r.id -and $r.ref -ne "security_csp") { $obj.id = $r.id }
  [pscustomobject]$obj
}

$updated = Invoke-CfApi -Method PUT -Path "/zones/$ZoneId/rulesets/phases/http_response_headers_transform/entrypoint" -Body @{
  rules = @($cleanRules)
}
Write-Host ("Updated entrypoint {0}; rules: {1}" -f $updated.id, @($updated.rules).Count)
@($updated.rules) | ForEach-Object {
  Write-Host (" - {0} / {1}" -f $_.ref, $_.description)
}
