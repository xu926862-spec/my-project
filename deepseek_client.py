#!/usr/bin/env python3
"""
统一 DeepSeek API 客户端
供本地功能性机器人调用，DeepSeek API 兼容 OpenAI 格式
"""

import os
import requests


def _load_dotenv(path=".env"):
    """极简 .env 加载器：把文件里的 KEY=VALUE 写进 os.environ（已存在的变量不覆盖）"""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


_load_dotenv()


class DeepSeekClient:
    """DeepSeek API 封装"""

    def __init__(self, system_prompt="你是一个有帮助的 AI 助手。", model="deepseek-chat"):
        self.api_key = os.environ.get("DEEPSEEK_API_KEY")
        self.system_prompt = system_prompt
        self.model = model
        self.base_url = "https://api.deepseek.com/v1/chat/completions"

    def available(self):
        """检查 API key 是否已配置"""
        return bool(self.api_key)

    def send(self, message, history=None, max_tokens=1024, temperature=0.7):
        """发送消息给 DeepSeek，返回文本回复"""
        if not self.api_key:
            raise RuntimeError("未设置 DEEPSEEK_API_KEY，无法调用 DeepSeek API")

        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": message})

        response = requests.post(
            self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    client = DeepSeekClient()
    if client.available():
        print("✓ DeepSeek API 已配置")
        reply = client.send("你好，请自我介绍一下")
        print(f"DeepSeek: {reply}")
    else:
        print("⚠️  未检测到 DEEPSEEK_API_KEY 环境变量")
        print("   在 .env 文件里添加: DEEPSEEK_API_KEY=你的key")
