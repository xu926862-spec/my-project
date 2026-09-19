# 🤖 多机器人系统设置指南

## 系统架构

```
┌─────────────────────────────────────┐
│  管理中心 (5000)                     │
│  ├─ 通用助手 (8001)                 │
│  ├─ 代码修复师 (8002)               │
│  ├─ 写作助手 (8003)                 │
│  ├─ 数据分析师 (8004)               │
│  └─ 教学助手 (8005)                 │
└─────────────────────────────────────┘
```

## 快速启动

### Linux / macOS

```bash
# 启动所有机器人
bash start_all_bots.sh

# 在浏览器打开
# http://localhost:5000
```

### Windows PowerShell

```powershell
# 启动管理中心
python multi_bot_manager.py

# 或在另一个窗口启动单个机器人
python claude_local_bot.py
python code_fixer_bot.py
```

## API 端点

### 管理中心

- **仪表板**: `GET http://localhost:5000/`
- **状态查询**: `GET http://localhost:5000/status`
- **机器人列表**: `GET http://localhost:5000/bots`

### 机器人端点

| 机器人 | 端口 | 用途 |
|-------|------|------|
| 通用助手 | 8001 | 闲聊、问答 |
| 代码修复师 | 8002 | 代码审查 |
| 写作助手 | 8003 | 文章生成 |
| 数据分析师 | 8004 | 数据处理 |
| 教学助手 | 8005 | 教学支持 |

## 使用示例

### 查询系统状态

```bash
curl http://localhost:5000/status
```

### 获取机器人列表

```bash
curl http://localhost:5000/bots
```

### 访问特定机器人

```bash
# 通用助手
curl http://localhost:8001/chat

# 代码修复师
curl http://localhost:8002/fix

# 写作助手
curl http://localhost:8003/write
```

## 配置修改

编辑 `multi_bot_manager.py` 中的 `BotConfig.BOTS` 字典来：
- 添加新机器人
- 修改端口
- 改变机器人名称
- 更新描述

## 监控和日志

管理中心会记录所有机器人的启动状态。查看实时状态：

```bash
# 持续监控
watch -n 2 'curl -s http://localhost:5000/status | jq'
```

## 故障排除

### 端口被占用

```bash
# 查看占用的端口
lsof -i :5000

# 或在 Windows 上
netstat -ano | findstr :5000

# 杀死进程
kill -9 <PID>
```

### 机器人无法启动

检查：
1. Python 环境是否正确
2. 依赖是否已安装
3. 端口是否可用
4. 文件是否存在

## 下一步

1. ✅ 启动系统
2. ✅ 访问仪表板 (http://localhost:5000)
3. ✅ 测试各个机器人
4. ✅ 添加自定义机器人

---

祝使用愉快！🚀
