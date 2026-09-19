import os
from claude_client import ClaudeClient

# 替换为你的真实 API Key
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-你要替换成真实的密钥"

try:
    client = ClaudeClient()
    print("正在呼叫满级 Claude...")
    response = client.send("你好，请证明你已经满级，只用一句话回答。")
    print("\n【Claude 回复】:")
    print(response)
except Exception as e:
    print(f"运行出错: {e}")
