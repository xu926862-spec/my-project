import os
import requests
from anthropic import Anthropic

class ClaudeClient:
    """Claude 客户端 - 支持本地 LLM 或 Claude API"""
    
    def __init__(self, model="llama2", use_local=True, local_url="http://localhost:11434"):
        self.use_local = use_local
        self.model = model
        self.local_url = local_url
        self.conversation_history = []
        self.system_prompt = "你是一个有帮助的 AI 助手。"
        
        if not use_local:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY 环境变量未设置")
            self.client = Anthropic(api_key=api_key)
    
    def send(self, message):
        self.conversation_history.append({"role": "user", "content": message})
        
        if self.use_local:
            try:
                response = requests.post(
                    f"{self.local_url}/api/generate",
                    json={"model": self.model, "prompt": message, "stream": False},
                    timeout=30
                )
                assistant_message = response.json()["response"]
            except Exception as e:
                return f"本地服务错误: {e}"
        else:
            response = self.client.messages.create(
                model=self.model, max_tokens=2048, system=self.system_prompt,
                messages=self.conversation_history
            )
            assistant_message = response.content[0].text
        
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message
    
    def clear_history(self):
        self.conversation_history = []
