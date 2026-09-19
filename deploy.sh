#!/bin/bash
# Claude Chatbot Deployment Script
# Usage: sudo bash deploy.sh <api-key>

set -e

API_KEY="${1:-}"
INSTALL_DIR="/opt/claude-chatbot"
SERVICE_NAME="claude-chatbot"
SERVICE_USER="claude-bot"

if [ -z "$API_KEY" ]; then
    echo "❌ Error: API key required"
    echo "Usage: sudo bash deploy.sh <anthropic-api-key>"
    exit 1
fi

echo "🚀 部署 Claude 聊天机器人..."
echo ""

# 1. 创建用户
echo "1️⃣ 创建系统用户..."
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd -r -s /bin/false -d "$INSTALL_DIR" "$SERVICE_USER"
    echo "   ✓ 用户 $SERVICE_USER 已创建"
else
    echo "   ✓ 用户 $SERVICE_USER 已存在"
fi

# 2. 创建安装目录
echo ""
echo "2️⃣ 创建安装目录..."
mkdir -p "$INSTALL_DIR"
echo "   ✓ 目录 $INSTALL_DIR 已创建"

# 3. 复制文件
echo ""
echo "3️⃣ 复制应用文件..."
cp claude_chatbot.py "$INSTALL_DIR/"
cp chatbot_requirements.txt "$INSTALL_DIR/"
cp example_chatbot_usage.py "$INSTALL_DIR/"
echo "   ✓ 文件已复制"

# 4. 安装依赖
echo ""
echo "4️⃣ 安装 Python 依赖..."
pip3 install -r "$INSTALL_DIR/chatbot_requirements.txt" -q
echo "   ✓ 依赖已安装"

# 5. 配置权限
echo ""
echo "5️⃣ 配置权限..."
chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"
chmod 750 "$INSTALL_DIR"
chmod 640 "$INSTALL_DIR"/*
echo "   ✓ 权限已配置"

# 6. 创建 systemd 服务
echo ""
echo "6️⃣ 安装 systemd 服务..."
sed "s|sk-ant-your-key-here|$API_KEY|g" claude-chatbot.service > /etc/systemd/system/$SERVICE_NAME.service
chmod 644 /etc/systemd/system/$SERVICE_NAME.service
systemctl daemon-reload
echo "   ✓ 服务已安装"

# 7. 启动服务
echo ""
echo "7️⃣ 启动服务..."
systemctl start "$SERVICE_NAME"
systemctl enable "$SERVICE_NAME"
echo "   ✓ 服务已启动并设置为自启"

# 8. 验证
echo ""
echo "8️⃣ 验证部署..."
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "   ✓ 服务运行正常"
else
    echo "   ❌ 服务启动失败"
    systemctl status "$SERVICE_NAME"
    exit 1
fi

echo ""
echo "✅ 部署完成！"
echo ""
echo "📋 服务管理命令:"
echo "   启动:    sudo systemctl start $SERVICE_NAME"
echo "   停止:    sudo systemctl stop $SERVICE_NAME"
echo "   重启:    sudo systemctl restart $SERVICE_NAME"
echo "   状态:    sudo systemctl status $SERVICE_NAME"
echo "   日志:    sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "📍 安装位置: $INSTALL_DIR"
echo "👤 运行用户: $SERVICE_USER"
