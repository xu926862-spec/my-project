#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Lightweight, dependency-free multi-provider AI caller (DeepSeek + Anthropic Claude).
.EXAMPLE
    multi_ai "write a python quicksort"
.EXAMPLE
    multi_ai "write a python quicksort" -Provider claude
.EXAMPLE
    multi_ai "continue" -Provider deepseek -Model deepseek-reasoner
.EXAMPLE
    echo "summarize this text" | multi_ai -Provider claude
#>

param(
    [Parameter(Position=0, ValueFromRemainingArguments=$true)]
    [string[]]$Prompt,

    [ValidateSet("deepseek", "claude")]
    [string]$Provider = "deepseek",

    [string]$Model = "",

    [int]$MaxTokens = 4096,

    [string]$System = "你是一个有帮助的助手。"
)

# --- Per-provider config ---
$ProviderConfig = @{
    deepseek = @{
        EnvKey       = "DEEPSEEK_API_KEY"
        KeyFile      = Join-Path $env:USERPROFILE ".claude-cli\deepseek-key.txt"
        Url          = "https://api.deepseek.com/v1/chat/completions"
        DefaultModel = "deepseek-chat"
        AuthHeader   = "Authorization"
        AuthPrefix   = "Bearer "
        ExtraHeaders = @{}
    }
    claude = @{
        EnvKey       = "ANTHROPIC_API_KEY"
        KeyFile      = Join-Path $env:USERPROFILE ".claude-cli\api-key.txt"
        Url          = "https://api.anthropic.com/v1/messages"
        DefaultModel = "claude-sonnet-5"
        AuthHeader   = "x-api-key"
        AuthPrefix   = ""
        ExtraHeaders = @{ "anthropic-version" = "2023-06-01" }
    }
}

$cfg = $ProviderConfig[$Provider]
if (-not $Model) { $Model = $cfg.DefaultModel }

# --- Resolve API key ---
$ApiKey = [Environment]::GetEnvironmentVariable($cfg.EnvKey)
if (-not $ApiKey -and (Test-Path $cfg.KeyFile)) {
    $ApiKey = (Get-Content $cfg.KeyFile -Raw).Trim()
}

if (-not $ApiKey) {
    Write-Host "[ERROR] No API key found for provider '$Provider'." -ForegroundColor Red
    Write-Host "Set it once with:" -ForegroundColor Yellow
    Write-Host "  `$env:$($cfg.EnvKey) = 'your-key'  # current session"
    Write-Host "  [Environment]::SetEnvironmentVariable('$($cfg.EnvKey)','your-key','User')  # permanent"
    Write-Host "Or save to: $($cfg.KeyFile)"
    exit 1
}

# --- Build message content ---
$userMessage = ""
if ($Prompt -and $Prompt.Count -gt 0) {
    $userMessage = ($Prompt -join " ")
} else {
    $userMessage = [Console]::In.ReadToEnd().Trim()
}

if (-not $userMessage) {
    Write-Host "[ERROR] No prompt provided." -ForegroundColor Red
    Write-Host "Usage: multi_ai `"your message here`" [-Provider deepseek|claude]"
    exit 1
}

# --- Build request body (provider-specific shape) ---
if ($Provider -eq "claude") {
    $body = @{
        model = $Model
        max_tokens = $MaxTokens
        system = $System
        messages = @(
            @{ role = "user"; content = $userMessage }
        )
    }
} else {
    $body = @{
        model = $Model
        max_tokens = $MaxTokens
        messages = @(
            @{ role = "system"; content = $System }
            @{ role = "user"; content = $userMessage }
        )
    }
}

$jsonBody = $body | ConvertTo-Json -Depth 10

$headers = @{ "content-type" = "application/json" }
$headers[$cfg.AuthHeader] = "$($cfg.AuthPrefix)$ApiKey"
foreach ($k in $cfg.ExtraHeaders.Keys) { $headers[$k] = $cfg.ExtraHeaders[$k] }

# --- Call API ---
try {
    $response = Invoke-WebRequest -Uri $cfg.Url `
        -Method Post `
        -Headers $headers `
        -Body $jsonBody `
        -UseBasicParsing `
        -TimeoutSec 120

    $result = $response.Content | ConvertFrom-Json

    if ($Provider -eq "claude") {
        $text = ($result.content | Where-Object { $_.type -eq "text" } | Select-Object -ExpandProperty text) -join "`n"
    } else {
        $text = $result.choices[0].message.content
    }
    Write-Output $text

    if ($env:MULTI_AI_VERBOSE) {
        Write-Host "`n[provider=$Provider model=$Model]" -ForegroundColor DarkGray
    }
}
catch {
    $statusCode = $null
    try { $statusCode = [int]$_.Exception.Response.StatusCode } catch {}
    Write-Host "[ERROR] Request failed (provider=$Provider, HTTP $statusCode)" -ForegroundColor Red

    if ($_.ErrorDetails -and $_.ErrorDetails.Message) {
        Write-Host $_.ErrorDetails.Message -ForegroundColor Red
    } else {
        Write-Host $_.Exception.Message -ForegroundColor Red
    }

    if ($statusCode -eq 401) {
        Write-Host "`n[HINT] 401 = invalid/expired API key for $Provider." -ForegroundColor Yellow
    } elseif ($statusCode -eq 404) {
        Write-Host "`n[HINT] 404 often means an invalid/retired model ID ('$Model')." -ForegroundColor Yellow
    }
    exit 1
}
