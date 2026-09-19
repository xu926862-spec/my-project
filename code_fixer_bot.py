import requests

class CodeFixerBot:
    """专业代码修复和优化助手"""
    
    def __init__(self):
        self.history = []
        self.system_prompt = """你是一个专业的代码审查和优化专家。能力包括：
- 分析和修复所有编程语言的代码
- 识别 bug 和性能问题
- 优化算法和代码结构
- 提供最佳实践建议
- 解释代码的工作原理

对每个问题都提供：
1. 问题分析（具体问题在哪）
2. 修复方案（如何解决）
3. 改进代码（修复后的代码）
4. 最佳实践（如何避免）"""
        self.base_url = "http://localhost:11434/api/generate"
    
    def send(self, message):
        self.history.append(message)
        context = self.system_prompt + "\n\n"
        for i, msg in enumerate(self.history[:-1]):
            role = "User" if i % 2 == 0 else "Assistant"
            context += f"{role}: {msg[:200]}...\n" if len(msg) > 200 else f"{role}: {msg}\n"
        context += f"User: {message}\nAssistant:"
        
        try:
            response = requests.post(
                self.base_url,
                json={"model": "llama2", "prompt": context, "stream": False},
                timeout=120
            )
            result = response.json()["response"].strip() if response.status_code == 200 else "Error"
            self.history.append(result)
            return result
        except Exception as e:
            return f"Error: {e}"
    
    def run(self):
        print("\n" + "="*60)
        print("🔧 代码修复助手 (由 Llama2 驱动)")
        print("="*60)
        print("用途: 粘贴代码, 我帮你分析、修复和优化")
        print("命令: /quit 退出, /clear 清空\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input == "/quit":
                    print("Goodbye! 👋")
                    break
                if user_input == "/clear":
                    self.history = []
                    print("✅ History cleared\n")
                    continue
                
                print("\nAssistant: ", end="", flush=True)
                response = self.send(user_input)
                print(response + "\n")
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break

if __name__ == "__main__":
    bot = CodeFixerBot()
    bot.run()
