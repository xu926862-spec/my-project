#!/usr/bin/env python3
"""
统一 Claude API 客户端
供所有机器人调用，支持 Claude API + 本地模型自动降级
"""

import os
from anthropic import Anthropic


class ClaudeAPIClient:
    """统一的 Claude API 封装，供多机器人系统复用"""

    def __init__(self, system_prompt="你是一个有帮助的 AI 助手。", model="claude-opus-5"):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.system_prompt = system_prompt
        self.model = model
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None

    def available(self):
        """检查 API 是否可用"""
        return self.client is not None

    def send(self, message, history=None, max_tokens=1024):
        """发送消息给 Claude，返回文本回复"""
        if not self.client:
            raise RuntimeError("未设置 ANTHROPIC_API_KEY，无法调用 Claude API")

        messages = list(history) if history else []
        messages.append({"role": "user", "content": message})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=self.system_prompt,
            messages=messages,
        )
        return response.content[0].text


if __name__ == "__main__":
    client = ClaudeAPIClient()
    if client.available():
        print("✓ Claude API 已配置")
        reply = client.send("你好，请自我介绍一下")
        print(f"Claude: {reply}")
    else:
        print("⚠️  未检测到 ANTHROPIC_API_KEY 环境变量")
        print("   设置方式: export ANTHROPIC_API_KEY=your_key_here")
        print("   各机器人将继续使用本地模型作为后备")
