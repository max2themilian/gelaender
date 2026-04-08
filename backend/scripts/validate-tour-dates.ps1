param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"

function Assert-True {
    param(
        [bool]$Condition,
        [string]$Message
    )

    if (-not $Condition) {
        throw $Message
    }
}

$endpoint = "$BaseUrl/api/tour-dates"
Write-Host "Requesting $endpoint"

$response = Invoke-RestMethod -Method Get -Uri $endpoint -TimeoutSec 15

Assert-True -Condition ($response -is [System.Array]) -Message "Response is not an array"
Assert-True -Condition ($response.Count -gt 0) -Message "Response array is empty"

$datePattern = '^\d{4}-\d{2}-\d{2}$'
$urlPattern = '^https?://'

for ($i = 0; $i -lt $response.Count; $i++) {
    $item = $response[$i]

    Assert-True -Condition ($null -ne $item.id) -Message "Item[$i] is missing id"
    Assert-True -Condition ($item.id -as [int]) -Message "Item[$i].id is not an int"
    Assert-True -Condition (-not [string]::IsNullOrWhiteSpace($item.event_name)) -Message "Item[$i].event_name is empty"
    Assert-True -Condition ($item.date -match $datePattern) -Message "Item[$i].date has invalid format (expected YYYY-MM-DD)"
    Assert-True -Condition (-not [string]::IsNullOrWhiteSpace($item.city)) -Message "Item[$i].city is empty"
    Assert-True -Condition (-not [string]::IsNullOrWhiteSpace($item.venue_name)) -Message "Item[$i].venue_name is empty"
    Assert-True -Condition ($item.ticket_url -match $urlPattern) -Message "Item[$i].ticket_url must start with http:// or https://"
}

Write-Host "Validation passed for $($response.Count) item(s)."
$response | Select-Object -First 3 | ConvertTo-Json -Depth 4
