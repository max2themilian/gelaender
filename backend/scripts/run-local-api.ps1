param(
    [string]$EnvPath = ".env",
    [string]$IcsUrl = "",
    [int]$ApiPort = 8000
)

$ErrorActionPreference = "Stop"

function Set-EnvFromFile {
    param([string]$Path)

    if (-not (Test-Path -Path $Path)) {
        return
    }

    Get-Content -Path $Path | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#")) {
            return
        }

        $splitIndex = $line.IndexOf("=")
        if ($splitIndex -lt 1) {
            return
        }

        $key = $line.Substring(0, $splitIndex).Trim()
        $value = $line.Substring($splitIndex + 1).Trim()

        if ($value.StartsWith('"') -and $value.EndsWith('"') -and $value.Length -ge 2) {
            $value = $value.Substring(1, $value.Length - 2)
        }

        [Environment]::SetEnvironmentVariable($key, $value, "Process")
    }
}

Set-EnvFromFile -Path $EnvPath

if (-not $env:GOOGLE_CALENDAR_ICS_URL -and $EnvPath -eq ".env") {
    $rootEnvPath = Join-Path $PSScriptRoot "..\..\.env"
    Set-EnvFromFile -Path $rootEnvPath
}

if (-not $env:APP_ENV) {
    $env:APP_ENV = "development"
}

if (-not $env:DATABASE_URL) {
    $env:DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
}

if (-not $env:ALLOWED_ORIGINS) {
    $env:ALLOWED_ORIGINS = '["http://127.0.0.1:5500","http://localhost:5500","http://127.0.0.1:3000"]'
}

if ($IcsUrl) {
    $env:GOOGLE_CALENDAR_ICS_URL = $IcsUrl
}

Write-Host "Starting FastAPI on http://127.0.0.1`:$ApiPort"
if ($env:GOOGLE_CALENDAR_ICS_URL) {
    Write-Host "Using ICS URL from env: GOOGLE_CALENDAR_ICS_URL is set"
}
else {
    Write-Host "GOOGLE_CALENDAR_ICS_URL is not set; endpoint will fall back to API key source, then static fixtures"
}

$pythonExe = Join-Path $PSScriptRoot "..\..\.venv\Scripts\python.exe"
if (-not (Test-Path -Path $pythonExe)) {
    $pythonExe = "python"
}

$backendRoot = Join-Path $PSScriptRoot ".."
Push-Location $backendRoot
try {
    & $pythonExe -m uvicorn app.main:app --reload --port $ApiPort
}
finally {
    Pop-Location
}
