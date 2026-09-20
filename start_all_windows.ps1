# Windows full system launcher
# Starts the manager plus all bots and the gateway

Write-Host "Starting multi-bot system (Windows)" -ForegroundColor Green
Write-Host ""

# Check Python
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found, please install Python first" -ForegroundColor Red
    exit
}

Write-Host "OK: Python installed: $pythonCheck" -ForegroundColor Green

# Create logs directory
if (!(Test-Path "logs")) {
    New-Item -ItemType Directory -Name "logs" | Out-Null
}

# Helper to launch one bot
function Start-Bot($name, $script, $port) {
    Write-Host "Starting $name (port $port)..." -ForegroundColor Cyan
    Start-Process python -ArgumentList $script -WindowStyle Minimized -NoNewWindow
    Start-Sleep -Seconds 1
}

# Start management center
Write-Host "Starting manager (port 5000)..." -ForegroundColor Yellow
Start-Process python -ArgumentList "multi_bot_manager.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start all bots
Start-Bot "Assistant" "claude_local_bot.py" "8001"
Start-Bot "Code Fixer" "code_fixer_bot.py" "8002"
Start-Bot "Summarizer" "summarizer_bot.py" "8006"
Start-Bot "Windows Gateway" "windows_gateway.py" "9000"

Write-Host ""
Write-Host "All services started!" -ForegroundColor Green
Write-Host ""
Write-Host "URLs:" -ForegroundColor Cyan
Write-Host "   Manager panel: http://localhost:5000" -ForegroundColor White
Write-Host "   Status API:    http://localhost:5000/status" -ForegroundColor White
Write-Host ""
Write-Host "Bot ports:" -ForegroundColor Cyan
Write-Host "   Assistant:   http://localhost:8001" -ForegroundColor White
Write-Host "   Code Fixer:  http://localhost:8002" -ForegroundColor White
Write-Host "   Summarizer:  http://localhost:8006" -ForegroundColor White
Write-Host "   Gateway:     http://localhost:9000" -ForegroundColor White
Write-Host ""
Write-Host "Note: all processes run in the background." -ForegroundColor Yellow
Write-Host "      Visible in Task Manager." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to stop all services..." -ForegroundColor Gray
[Console]::ReadKey() | Out-Null

# Stop all python processes
Write-Host ""
Write-Host "Stopping all services..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "OK: all services stopped" -ForegroundColor Green
