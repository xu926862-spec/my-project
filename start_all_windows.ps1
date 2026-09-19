# Windows 完整系统启动脚本
# 同时启动所有机器人和网关

Write-Host "🚀 启动多机器人完整系统 (Windows)" -ForegroundColor Green
Write-Host ""

# 检查 Python
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 未找到 Python，请先安装 Python" -ForegroundColor Red
    exit
}

Write-Host "✓ Python 已安装: $pythonCheck" -ForegroundColor Green

# 创建日志目录
if (!(Test-Path "logs")) {
    New-Item -ItemType Directory -Name "logs" | Out-Null
}

# 启动函数
function Start-Bot($name, $script, $port) {
    Write-Host "🤖 启动 $name (端口 $port)..." -ForegroundColor Cyan
    Start-Process python -ArgumentList $script -WindowStyle Minimized -NoNewWindow
    Start-Sleep -Seconds 1
}

# 启动管理中心
Write-Host "📡 启动管理中心 (端口 5000)..." -ForegroundColor Yellow
Start-Process python -ArgumentList "multi_bot_manager.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# 启动所有机器人
Start-Bot "通用助手" "claude_local_bot.py" "8001"
Start-Bot "代码修复师" "code_fixer_bot.py" "8002"
Start-Bot "总结助手" "summarizer_bot.py" "8006"
Start-Bot "Windows 网关" "windows_gateway.py" "9000"

Write-Host ""
Write-Host "✅ 所有服务已启动！" -ForegroundColor Green
Write-Host ""
Write-Host "📊 访问地址：" -ForegroundColor Cyan
Write-Host "   管理面板: http://localhost:5000" -ForegroundColor White
Write-Host "   状态 API: http://localhost:5000/status" -ForegroundColor White
Write-Host ""
Write-Host "🤖 机器人端口：" -ForegroundColor Cyan
Write-Host "   通用助手:    http://localhost:8001" -ForegroundColor White
Write-Host "   代码修复师:  http://localhost:8002" -ForegroundColor White
Write-Host "   总结助手:    http://localhost:8006" -ForegroundColor White
Write-Host "   网关:       http://localhost:9000" -ForegroundColor White
Write-Host ""
Write-Host "📝 提示：所有进程运行在后台。" -ForegroundColor Yellow
Write-Host "        在任务管理器中可见。" -ForegroundColor Yellow
Write-Host ""
Write-Host "按任意键停止所有服务..." -ForegroundColor Gray
[Console]::ReadKey() | Out-Null

# 停止所有 Python 进程
Write-Host ""
Write-Host "🛑 停止所有服务..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "✓ 所有服务已停止" -ForegroundColor Green
