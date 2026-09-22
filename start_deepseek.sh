#!/bin/bash
# DeepSeek API 快速启动脚本
# 自动设置环境并启动交互式处理系统

set -e

echo "🚀 DeepSeek API 启动系统"
echo "=========================="
echo ""

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    exit 1
fi

echo "✓ Python 3 已检测"

# 检查 API 密钥
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo ""
    echo "⚠️  未设置 DEEPSEEK_API_KEY 环境变量"
    echo ""
    echo "请设置您的 DeepSeek API 密钥:"
    echo "  export DEEPSEEK_API_KEY='sk-your-api-key'"
    echo ""
    echo "然后重新运行此脚本"
    exit 1
fi

echo "✓ API 密钥已检测 (长度: ${#DEEPSEEK_API_KEY})"
echo ""

# 显示菜单
echo "请选择启动模式:"
echo ""
echo "1️⃣  交互式文本处理 (推荐)"
echo "2️⃣  Claude Bot CLI"
echo "3️⃣  测试 API 连接"
echo ""

read -p "请选择 (1-3) [1]: " choice
choice=${choice:-1}

echo ""

case $choice in
    1)
        echo "🚀 启动交互式文本处理系统..."
        python3 interactive_deepseek.py
        ;;
    2)
        echo "🚀 启动 Claude Bot..."
        cd claude_bot_v3.5
        python3 claude_bot.py chat
        ;;
    3)
        echo "🧪 测试 API 连接..."
        python3 test_deepseek_api.py
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "✓ 已完成"
