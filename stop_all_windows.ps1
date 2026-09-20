# Stops all bot/manager python processes started by start_all_windows.ps1

Write-Host "Stopping all services..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "OK: all services stopped" -ForegroundColor Green
