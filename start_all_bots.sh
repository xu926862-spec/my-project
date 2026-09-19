#!/bin/bash
# 启动所有机器人系统

echo "🚀 启动多机器人系统..."
echo ""

# 启动管理中心
echo "📡 启动管理中心 (端口 5000)..."
python3 multi_bot_manager.py &
MANAGER_PID=$!

# 等待管理中心启动
sleep 2

echo ""
echo "✅ 系统已启动！"
echo ""
echo "📊 管理面板: http://localhost:5000"
echo "📊 状态查询: http://localhost:5000/status"
echo "📋 机器人列表: http://localhost:5000/bots"
echo ""
echo "🤖 机器人端口："
echo "   - 通用助手: :8001"
echo "   - 代码修复: :8002"
echo "   - 写作助手: :8003"
echo "   - 数据分析: :8004"
echo "   - 教学助手: :8005"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待进程
wait $MANAGER_PID
