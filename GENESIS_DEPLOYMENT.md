# Genesis Omniscience System - 部署指南

## 🌌 系统概述

**Genesis Omniscience v3.0-ULTIMATE** 是最先进的本地 AI 智能系统，具备：
- 多模型智能编排
- 自我优化和进化
- 知识图谱系统
- 自愈容错机制
- 完整监控告警

## 📋 前置要求

### 系统要求
- Python 3.9+
- 4GB+ RAM
- 2GB+ 磁盘空间
- Linux/macOS/WSL2 推荐

### 软件依赖
```bash
pip3 install openai asyncio aiohttp
```

### 本地模型服务
需要运行 **Llama 模型服务**：
```bash
# 选项1: 通过 Ollama
ollama pull llama2
ollama serve

# 选项2: 通过 llama.cpp
llama-server -m model.gguf -ngl 33 -p 8000
```

## 🚀 快速部署

### 第一步：运行部署脚本
```bash
cd /home/user/my-project
chmod +x deploy_genesis.sh
./deploy_genesis.sh
```

这个脚本会自动：
- ✅ 检查所有依赖
- ✅ 初始化目录结构
- ✅ 验证配置文件
- ✅ 检查 Llama 服务
- ✅ 初始化数据库
- ✅ 运行诊断测试
- ✅ 生成启动脚本
- ✅ 配置 systemd 服务

### 第二步：启动系统

**方式1：交互模式（推荐开发）**
```bash
python3 genesis_omniscience.py
```

**方式2：使用启动脚本**
```bash
./start_genesis.sh
```

**方式3：作为后台服务（推荐生产）**
```bash
# 启用服务
systemctl --user enable genesis
systemctl --user start genesis

# 查看日志
journalctl --user -u genesis -f

# 停止服务
systemctl --user stop genesis
```

## 📊 验证部署

### 健康检查
```bash
python3 health_check_genesis.py
```

输出示例：
```json
{
  "name": "Genesis Omniscience",
  "version": "3.0-ULTIMATE",
  "status": "OPERATIONAL",
  "health": {
    "status": "HEALTHY",
    "recent_errors": 0
  },
  "quality_score": 9.8
}
```

### 日志位置
```
~/.genesis/logs/genesis.log
```

### 数据库位置
```
~/.genesis/knowledge.db
```

## 🎯 使用示例

### 基础对话
```python
from genesis_omniscience import GenesisOmniscience

genesis = GenesisOmniscience()

# 标准查询
response = genesis.chat("设计一个高性能系统")
print(response)
```

### 集合预测（多模型投票）
```python
import asyncio

async def ensemble_mode():
    genesis = GenesisOmniscience()
    
    # 使用多个模型进行投票
    result = await genesis.process_query("复杂架构问题", use_ensemble=True)
    print(result)

asyncio.run(ensemble_mode())
```

### 自我优化
```python
import asyncio

async def self_optimize():
    genesis = GenesisOmniscience()
    
    # 分析性能并自动改进
    await genesis.trigger_self_optimization()

asyncio.run(self_optimize())
```

### 获取系统状态
```python
genesis = GenesisOmniscience()

# 完整系统状态
status = genesis.get_system_status()
print(f"质量评分: {status['quality_score']}/10")
print(f"请求数: {status['requests']}")

# 导出完整数据
export = genesis.export_complete_state()
```

## ⚙️ 配置调整

编辑 `genesis.config.json`：

### 性能优化
```json
{
  "performance": {
    "max_tokens": 8192,
    "concurrent_requests": 20,
    "cache_enabled": true,
    "cache_size_mb": 2048
  }
}
```

### 监控告警
```json
{
  "monitoring": {
    "alert_thresholds": {
      "response_time": 3.0,
      "error_rate": 0.02,
      "quality_score": 8.0
    }
  }
}
```

### 自进化
```json
{
  "evolution": {
    "self_optimization": true,
    "optimization_interval": 1800,
    "quality_improvement_target": 9.9
  }
}
```

## 🔍 监控和维护

### 查看实时日志
```bash
tail -f ~/.genesis/logs/genesis.log
```

### 性能指标
系统会自动收集：
- 响应时间
- 质量评分
- 错误率
- 缓存命中率
- 吞吐量

### 定期检查
```bash
# 每天检查一次
0 0 * * * python3 /home/user/my-project/health_check_genesis.py
```

## 🆘 故障排查

### 问题：Llama 服务未连接
```
解决方案：
1. 检查 Llama 服务是否运行
2. 检查端口 8000 是否打开
3. 在配置中修改 base_url

# 测试连接
curl http://localhost:8000/v1/models
```

### 问题：数据库锁定
```
解决方案：
1. 停止 Genesis
2. 删除数据库：rm ~/.genesis/knowledge.db
3. 重新启动
```

### 问题：内存使用过高
```
解决方案：
1. 减小 cache_size_mb（genesis.config.json）
2. 减少 max_tokens
3. 启用缓存过期策略
```

### 查看完整错误
```bash
python3 genesis_omniscience.py --debug
```

## 📈 性能优化建议

### 1. 启用 GPU 加速
```json
{
  "llama": {
    "gpu_layers": 33,
    "context_size": 8192
  }
}
```

### 2. 缓存优化
```json
{
  "performance": {
    "cache_size_mb": 4096,
    "cache_ttl_seconds": 3600
  }
}
```

### 3. 并发优化
```json
{
  "performance": {
    "concurrent_requests": 50,
    "batch_size": 10
  }
}
```

## 🔐 安全配置

### 启用认证
```json
{
  "security": {
    "enable_auth": true,
    "api_key": "your-secret-key"
  }
}
```

### 启用速率限制
```json
{
  "security": {
    "rate_limiting": true,
    "requests_per_minute": 60
  }
}
```

### 启用加密
```json
{
  "security": {
    "data_encryption": true,
    "tls_enabled": true
  }
}
```

## 📚 API 接口

### 对话接口
```python
genesis.chat(user_input: str, stream: bool = False) -> str
```

### 查询接口
```python
await genesis.process_query(query: str, use_ensemble: bool = False) -> str
```

### 知识库接口
```python
genesis.knowledge_graph.add_node(concept: str, description: str)
genesis.knowledge_graph.add_relation(source, target, relation, weight)
genesis.knowledge_graph.find_pattern_chain(start_concept, depth)
```

### 监控接口
```python
genesis.get_system_status() -> Dict
genesis.monitoring.get_dashboard_data() -> Dict
genesis.healing_system.get_health_status() -> Dict
```

## 🌟 高级功能

### 1. 多模型集合
系统会自动选择最适合的模型，也支持集合投票。

### 2. 知识图谱
自动构建和维护概念关系，支持模式链发现。

### 3. 自优化
系统会自动分析性能并建议改进。

### 4. 自愈
出错时自动尝试恢复。

### 5. 完全可观测
实时监控、详细日志、性能指标。

## 📞 支持和反馈

- 查看日志：`~/.genesis/logs/genesis.log`
- 检查配置：`genesis.config.json`
- 运行诊断：`python3 health_check_genesis.py`

## 🎉 部署完成

恭喜！Genesis Omniscience 已成功部署。

```
🌌 GOD MODE ACTIVATED ✨
系统已就绪，等待您的指令。
```

---

**版本**: Genesis Omniscience v3.0-ULTIMATE  
**状态**: 📍 Production Ready  
**模式**: 🔮 GOD MODE ACTIVE
