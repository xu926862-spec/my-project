import os
import json
import requests
from anthropic import Anthropic

class HybridClaudeBot:
    """混合 Claude - 优先用 Claude API，备选本地 LLM"""
    
    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.conversation_history = []
        self.system_prompt = "你是一个有帮助的 AI 助手。"
        self.mode = None
        self.init_mode()
    
    def init_mode(self):
        """自动选择运行模式"""
        if self.api_key and self._test_claude_api():
            self.client = Anthropic(api_key=self.api_key)
            self.mode = "Claude API"
            print("✅ 使用 Claude API (云端)")
        elif self._test_local_llm():
            self.mode = "Local Ollama"
            print("✅ 使用本地 Llama2 (本地)")
        else:
            raise RuntimeError("❌ 无法连接 Claude API 也无法连接本地 LLM")
    
    def _test_claude_api(self):
        """测试 Claude API 连接"""
        try:
            client = Anthropic(api_key=self.api_key)
            client.messages.create(
                model="claude-opus-5",
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
        except:
            return False
    
    def _test_local_llm(self):
        """测试本地 LLM 连接"""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama2", "prompt": "test", "stream": False},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def send(self, message):
        """发送消息"""
        self.conversation_history.append({"role": "user", "content": message})
        
        if self.mode == "Claude API":
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=2048,
                system=self.system_prompt,
                messages=self.conversation_history
            )
            assistant_message = response.content[0].text
        else:  # Local Ollama
            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "llama2", "prompt": message, "stream": False},
                    timeout=30
                )
                assistant_message = response.json()["response"]
            except Exception as e:
                return f"❌ 本地服务错误: {e}"
        
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message
    
    def interactive_chat(self):
        """交互式聊天"""
        print("\n" + "="*50)
        print(f"🤖 {self.mode} 聊天机器人")
        print("="*50)
        print("命令: /quit 退出, /clear 清空\n")
        
        while True:
            try:
                user_input = input("你: ").strip()
                if not user_input:
                    continue
                if user_input == "/quit":
                    print("再见! 💙\n")
                    break
                if user_input == "/clear":
                    self.conversation_history = []
                    print("✅ 历史已清空\n")
                    continue
                
                print("机器人: ", end="", flush=True)
                response = self.send(user_input)
                print(response + "\n")
            except KeyboardInterrupt:
                print("\n再见! 💙\n")
                break

if __name__ == "__main__":
    bot = HybridClaudeBot()
    bot.interactive_chat()
