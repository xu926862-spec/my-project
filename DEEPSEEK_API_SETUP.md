# 🚀 DeepSeek API 接入指南

## 📋 快速开始

### 步骤1: 获取 DeepSeek API 密钥

1. 访问 [DeepSeek 官网](https://www.deepseek.com)
2. 注册账户或登录
3. 进入 API 管理后台
4. 生成 API 密钥

### 步骤2: 配置环境

```bash
# 设置 DeepSeek API 密钥
export DEEPSEEK_API_KEY='sk-your-api-key-here'

# 验证配置
echo $DEEPSEEK_API_KEY
```

### 步骤3: 运行 Claude Bot

```bash
cd claude_bot_v3.5
python3 claude_bot.py chat "Hello, DeepSeek!"
```

## 🔐 API 配置详解

### API 端点

```
https://api.deepseek.com/v1/chat/completions
```

### 认证方式

```
Authorization: Bearer {DEEPSEEK_API_KEY}
Content-Type: application/json
```

### 请求格式

```json
{
  "model": "deepseek-chat",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Hello!"
    }
  ],
  "temperature": 0.5,
  "top_p": 0.95,
  "frequency_penalty": 0,
  "presence_penalty": 0,
  "stream": false
}
```

### 响应格式

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "deepseek-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Response text"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

## 🎯 可用模型

### 标准模型
- **deepseek-chat** - 通用聊天模型
  - 适合：一般问答、文本处理
  - 上下文：8K tokens
  - 价格：标准价格

### 推理模型
- **deepseek-reasoner-1215** - 高级推理模型（DeepSeek 3.5）
  - 适合：复杂问题、代码分析
  - 上下文：16K tokens
  - 特性：深层思考和推理

### 代码模型
- **deepseek-coder-67b** - 代码专家模型
  - 适合：代码生成、分析、调试
  - 上下文：8K tokens
  - 特性：多语言代码支持

## 📊 使用示例

### 示例1: 基础聊天

```bash
python3 claude_bot.py chat "你好，请介绍一下自己"
```

### 示例2: 使用推理模型

```bash
python3 claude_bot.py chat --model reasoner "分析这个数学问题的复杂性"
```

### 示例3: 代码分析

```bash
python3 claude_bot.py analyze code.py --model coder
```

### 示例4: 自定义系统提示

```bash
python3 claude_bot.py chat --system "你是一个Python专家" "如何优化这个函数？"
```

## 💰 定价和配额

### 按需付费模型

| 模型 | 输入价格 | 输出价格 | 备注 |
|------|---------|---------|------|
| deepseek-chat | $0.14/M | $0.28/M | 标准聊天 |
| deepseek-reasoner | $0.55/M | $2.19/M | 高级推理 |
| deepseek-coder | $0.14/M | $0.28/M | 代码专家 |

**注**: M = 百万 tokens

### 配额限制

- 免费账户：$1 额度
- 充值后：根据所选套餐

## 🔍 故障排查

### 问题1: API密钥无效
```
[Error] API Error: 401 Unauthorized
```

**解决方案**:
- 检查密钥是否正确复制
- 验证环境变量设置
- 确认密钥未过期

### 问题2: 超时错误
```
[Error] API Error: timeout
```

**解决方案**:
- 检查网络连接
- 减少请求长度
- 使用 chat 模型而不是 reasoner

### 问题3: 模型不可用
```
[Error] API Error: 404 Model not found
```

**解决方案**:
- 确保使用正确的模型名称
- 运行 `python3 claude_bot.py models` 查看可用模型
- 检查模型是否在您的地区可用

## 📈 性能优化

### 1. 使用适当的温度参数

```
temperature: 0.1  - 更确定的回复（事实性）
temperature: 0.5  - 平衡（推荐）
temperature: 0.9  - 更创意的回复
```

### 2. 控制输入长度

- 限制消息长度以加快响应
- 使用 `top_p` 参数进行核心采样

### 3. 批量请求

```bash
# 处理多个文件
python3 claude_bot.py analyze file1.py --no-review
python3 claude_bot.py analyze file2.py --no-review
```

## 🔗 相关资源

- [DeepSeek 官网](https://www.deepseek.com)
- [API 文档](https://api.deepseek.com/docs)
- [模型能力对比](https://www.deepseek.com/models)
- [定价信息](https://www.deepseek.com/pricing)

## ✅ 检查清单

在投入生产环境前，请确保：

- [ ] 已获得有效的 DeepSeek API 密钥
- [ ] 已正确设置环境变量
- [ ] 已充值足够的额度
- [ ] 已测试基本的 chat 功能
- [ ] 已测试所需的模型
- [ ] 已设置错误监控和日志记录
- [ ] 已配置超时保护
- [ ] 已进行负载测试

## 🎊 接入成功

一旦完成以上步骤，您就可以：

1. 使用 DeepSeek 3.5 模型
2. 进行实时聊天和分析
3. 集成到自己的应用中
4. 监控 API 使用统计

---

**祝使用愉快！🚀**
