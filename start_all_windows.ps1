# Windows full system launcher
# Starts the manager plus all bots and the gateway, then exits.
# Use stop_all_windows.ps1 to stop everything later.

Write-Host "Starting multi-bot system (Windows)" -ForegroundColor Green
Write-Host ""

# Check Python
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found, please install Python first" -ForegroundColor Red
    exit
}

Write-Host "OK: Python installed: $pythonCheck" -ForegroundColor Green

# Helper to launch one bot in its own minimized window
function Start-Bot($name, $script, $port) {
    Write-Host "Starting $name (port $port)..." -ForegroundColor Cyan
    Start-Process python -ArgumentList $script -WindowStyle Minimized
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
Start-Bot "Legal" "legal_bot.py" "8007"
Start-Bot "Medical" "medical_bot.py" "8008"
Start-Bot "Finance" "finance_bot.py" "8009"
Start-Bot "DeepSeek" "deepseek_bot.py" "8010"
Start-Bot "Local Claude" "local_claude_bot.py" "8011"
Start-Bot "Windows Gateway" "windows_gateway.py" "9000"

Write-Host ""
Write-Host "All services started!" -ForegroundColor Green
Write-Host ""
Write-Host "URLs:" -ForegroundColor Cyan
Write-Host "   Manager panel: http://localhost:5000" -ForegroundColor White
Write-Host "   Status API:    http://localhost:5000/status" -ForegroundColor White
Write-Host ""
Write-Host "Bot ports:" -ForegroundColor Cyan
Write-Host "   Assistant:    http://localhost:8001" -ForegroundColor White
Write-Host "   Code Fixer:   http://localhost:8002" -ForegroundColor White
Write-Host "   Summarizer:   http://localhost:8006" -ForegroundColor White
Write-Host "   Legal:        http://localhost:8007" -ForegroundColor White
Write-Host "   Medical:      http://localhost:8008" -ForegroundColor White
Write-Host "   Finance:      http://localhost:8009" -ForegroundColor White
Write-Host "   DeepSeek:     http://localhost:8010" -ForegroundColor White
Write-Host "   Local Claude: http://localhost:8011" -ForegroundColor White
Write-Host "   Gateway:      http://localhost:9000" -ForegroundColor White
Write-Host ""
Write-Host "All processes run in the background (minimized windows)." -ForegroundColor Yellow
Write-Host "This script has now exited - your terminal is free to use." -ForegroundColor Yellow
Write-Host "Run stop_all_windows.ps1 to stop everything later." -ForegroundColor Yellow
