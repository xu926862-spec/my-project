# Claude 聊天机器人 - 部署指南

## 系统服务部署（Linux/macOS）

### 前置要求

- Linux 系统（Ubuntu 20.04+, CentOS 7+）或 macOS
- Python 3.8+
- sudo 权限
- Anthropic API 密钥

### 快速部署（3 步）

#### 1. 获取 API 密钥

```bash
# 从 https://console.anthropic.com/account/keys 复制你的 API 密钥
# 格式: sk-ant-...
```

#### 2. 运行部署脚本

```bash
cd /path/to/my-project
sudo bash deploy.sh sk-ant-your-actual-key-here
```

#### 3. 验证部署

```bash
# 检查服务状态
sudo systemctl status claude-chatbot

# 查看实时日志
sudo journalctl -u claude-chatbot -f
```

---

## 服务管理

### 启动/停止/重启

```bash
# 启动服务
sudo systemctl start claude-chatbot

# 停止服务
sudo systemctl stop claude-chatbot

# 重启服务
sudo systemctl restart claude-chatbot

# 查看状态
sudo systemctl status claude-chatbot

# 启用/禁用自启
sudo systemctl enable claude-chatbot
sudo systemctl disable claude-chatbot
```

### 查看日志

```bash
# 实时日志
sudo journalctl -u claude-chatbot -f

# 最近 100 行
sudo journalctl -u claude-chatbot -n 100

# 今天的日志
sudo journalctl -u claude-chatbot --since today

# 错误日志
sudo journalctl -u claude-chatbot -p err
```

---

## 手动配置（如果不想使用脚本）

### 1. 创建系统用户

```bash
sudo useradd -r -s /bin/false -d /opt/claude-chatbot claude-bot
```

### 2. 准备应用目录

```bash
sudo mkdir -p /opt/claude-chatbot
sudo cp claude_chatbot.py /opt/claude-chatbot/
sudo cp chatbot_requirements.txt /opt/claude-chatbot/
sudo pip3 install -r /opt/claude-chatbot/chatbot_requirements.txt
sudo chown -R claude-bot:claude-bot /opt/claude-chatbot
```

### 3. 创建 systemd 服务文件

```bash
sudo nano /etc/systemd/system/claude-chatbot.service
```

复制下面的内容（替换 API 密钥）：

```ini
[Unit]
Description=Claude API Chatbot Service
After=network.target

[Service]
Type=simple
User=claude-bot
WorkingDirectory=/opt/claude-chatbot
ExecStart=/usr/bin/python3 /opt/claude-chatbot/claude_chatbot.py
Environment="ANTHROPIC_API_KEY=sk-ant-your-key"
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. 启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl start claude-chatbot
sudo systemctl enable claude-chatbot
```

---

## 环境变量配置

### 方式 1：systemd 服务文件

编辑 `/etc/systemd/system/claude-chatbot.service`：

```ini
[Service]
Environment="ANTHROPIC_API_KEY=sk-ant-..."
Environment="PYTHONUNBUFFERED=1"
```

### 方式 2：环境文件

创建 `/opt/claude-chatbot/.env`：

```bash
ANTHROPIC_API_KEY=sk-ant-...
PYTHONUNBUFFERED=1
```

然后在服务文件中：

```ini
[Service]
EnvironmentFile=/opt/claude-chatbot/.env
```

---

## 性能优化

### 内存使用

```bash
# 查看进程内存
ps aux | grep claude-chatbot

# 限制内存（可选）
# 在服务文件中添加：
# MemoryLimit=512M
```

### CPU 限制

```bash
# 在服务文件中添加：
# CPUQuota=50%
```

### 日志轮转

创建 `/etc/logrotate.d/claude-chatbot`：

```
/var/log/claude-chatbot*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 claude-bot claude-bot
}
```

---

## 常见问题

### Q: 服务无法启动

**A:** 查看日志：
```bash
sudo journalctl -u claude-chatbot -n 50
```

常见原因：
- API 密钥无效
- Python 版本过低
- 依赖未安装

### Q: 如何更新代码

**A:** 
```bash
# 1. 停止服务
sudo systemctl stop claude-chatbot

# 2. 更新文件
sudo cp claude_chatbot.py /opt/claude-chatbot/

# 3. 重启服务
sudo systemctl start claude-chatbot
```

### Q: 如何更换 API 密钥

**A:**
```bash
# 编辑服务文件
sudo nano /etc/systemd/system/claude-chatbot.service

# 修改 Environment 行，然后：
sudo systemctl daemon-reload
sudo systemctl restart claude-chatbot
```

### Q: 如何卸载

**A:**
```bash
# 停止并禁用服务
sudo systemctl stop claude-chatbot
sudo systemctl disable claude-chatbot

# 删除服务文件
sudo rm /etc/systemd/system/claude-chatbot.service
sudo systemctl daemon-reload

# 删除应用目录
sudo rm -rf /opt/claude-chatbot

# 删除用户（可选）
sudo userdel claude-bot
```

---

## 监控和告警

### 使用 systemd 日志进行监控

```bash
# 监控服务状态变化
sudo journalctl -u claude-chatbot -f --lines=0
```

### 创建监控脚本

创建 `/usr/local/bin/check-chatbot.sh`：

```bash
#!/bin/bash
if ! systemctl is-active --quiet claude-chatbot; then
    echo "Claude Chatbot is down!" | mail -s "Alert" admin@example.com
    systemctl restart claude-chatbot
fi
```

添加到 crontab：

```bash
*/5 * * * * /usr/local/bin/check-chatbot.sh
```

---

## 安全最佳实践

1. **API 密钥保护**
   - 使用环境变量，不要硬编码
   - 定期轮换密钥
   - 使用 systemd 的 ProtectHome=true

2. **文件权限**
   ```bash
   chmod 750 /opt/claude-chatbot
   chmod 640 /opt/claude-chatbot/*
   chown -R claude-bot:claude-bot /opt/claude-chatbot
   ```

3. **日志安全**
   - 定期轮转日志
   - 限制日志访问权限
   - 备份重要日志

4. **网络隔离**
   - 服务仅监听 localhost（默认）
   - 使用防火墙限制访问
   - 启用 HTTPS（如需远程访问）

---

## 升级服务

### 更新应用代码

```bash
cd /home/user/my-project
git pull origin claude/claude-rc-eurwt4
sudo cp claude_chatbot.py /opt/claude-chatbot/
sudo systemctl restart claude-chatbot
```

### 更新依赖

```bash
sudo pip3 install --upgrade -r /opt/claude-chatbot/chatbot_requirements.txt
sudo systemctl restart claude-chatbot
```

---

## 支持和反馈

- 📖 文档: `/opt/claude-chatbot/CHATBOT_README.md`
- 📝 快速开始: `/opt/claude-chatbot/QUICKSTART.md`
- 🐛 问题报告: https://github.com/xu926862-spec/my-project/issues

---

**部署完成！** 🎉 服务已在后台运行。
