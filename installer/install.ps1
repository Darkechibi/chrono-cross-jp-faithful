# Apply the JP-faithful Chrono Cross language pack (Steam Radical Dreamers Edition).
# Re-run after Steam Verify Integrity / redownload.
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
if (-not $py) {
    Write-Error "Python 3 is required. Install from https://www.python.org/downloads/"
}

& $py.Source "$here\install.py" @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""
Write-Host "If Steam ever restores English, run this installer again."
