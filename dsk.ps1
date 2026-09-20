#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Lightweight, dependency-free DeepSeek API caller.
.EXAMPLE
    dsk "write a python quicksort"
.EXAMPLE
    dsk "continue" -Model deepseek-reasoner
.EXAMPLE
    echo "summarize this text" | dsk
#>

param(
    [Parameter(Position=0, ValueFromRemainingArguments=$true)]
    [string[]]$Prompt,

    [string]$Model = "deepseek-chat",

    [int]$MaxTokens = 4096,

    [string]$System = "你是一个有帮助的助手。",

    [switch]$Stream
)

# --- Config: API key resolution order ---
# 1. Environment variable DEEPSEEK_API_KEY
# 2. Key file at ~/.claude-cli/deepseek-key.txt
$ApiKey = $env:DEEPSEEK_API_KEY
$KeyFile = Join-Path $env:USERPROFILE ".claude-cli\deepseek-key.txt"

if (-not $ApiKey -and (Test-Path $KeyFile)) {
    $ApiKey = (Get-Content $KeyFile -Raw).Trim()
}

if (-not $ApiKey) {
    Write-Host "[ERROR] No API key found." -ForegroundColor Red
    Write-Host "Set it once with:" -ForegroundColor Yellow
    Write-Host "  `$env:DEEPSEEK_API_KEY = 'sk-...'  # current session"
    Write-Host "  [Environment]::SetEnvironmentVariable('DEEPSEEK_API_KEY','sk-...','User')  # permanent"
    Write-Host "Or save to: $KeyFile"
    exit 1
}

# --- Build message content ---
$userMessage = ""
if ($Prompt -and $Prompt.Count -gt 0) {
    $userMessage = ($Prompt -join " ")
} else {
    # Read from stdin (pipe)
    $userMessage = [Console]::In.ReadToEnd().Trim()
}

if (-not $userMessage) {
    Write-Host "[ERROR] No prompt provided." -ForegroundColor Red
    Write-Host "Usage: dsk `"your message here`""
    exit 1
}

# --- Build request body (OpenAI-compatible format) ---
$body = @{
    model = $Model
    max_tokens = $MaxTokens
    messages = @(
        @{ role = "system"; content = $System }
        @{ role = "user"; content = $userMessage }
    )
}

$jsonBody = $body | ConvertTo-Json -Depth 10

$headers = @{
    "Authorization" = "Bearer $ApiKey"
    "content-type" = "application/json"
}

# --- Call API ---
try {
    $response = Invoke-WebRequest -Uri "https://api.deepseek.com/v1/chat/completions" `
        -Method Post `
        -Headers $headers `
        -Body $jsonBody `
        -UseBasicParsing `
        -TimeoutSec 120

    $result = $response.Content | ConvertFrom-Json
    $text = $result.choices[0].message.content
    Write-Output $text

    if ($env:DSK_VERBOSE) {
        Write-Host "`n[usage] input=$($result.usage.prompt_tokens) output=$($result.usage.completion_tokens)" -ForegroundColor DarkGray
    }
}
catch {
    $statusCode = $null
    try { $statusCode = [int]$_.Exception.Response.StatusCode } catch {}
    Write-Host "[ERROR] Request failed (HTTP $statusCode)" -ForegroundColor Red

    if ($_.ErrorDetails -and $_.ErrorDetails.Message) {
        Write-Host $_.ErrorDetails.Message -ForegroundColor Red
    } else {
        Write-Host $_.Exception.Message -ForegroundColor Red
    }

    if ($statusCode -eq 401) {
        Write-Host "`n[HINT] 401 = invalid/expired API key. Check the key in $KeyFile" -ForegroundColor Yellow
    }
    exit 1
}
