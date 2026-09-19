from claude_client import ClaudeClient

client = ClaudeClient(model="llama2", use_local=True)
print("正在调用本地 LLM...")
response = client.send("你好，请用一句话自我介绍。")
print("回复:", response)
