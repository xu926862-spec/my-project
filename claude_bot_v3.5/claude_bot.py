#!/usr/bin/env python3
"""
Claude Local Bot v3.5 (DeepSeek Integration) - Prototype
Focus: CLI Interaction, DeepSeek/OpenAI Compatible API, Code Analysis Skeleton
"""

import os
import sys
import json
import argparse
import urllib.request
from typing import Optional

# --- 配置区域 ---
# 切换为支持 DeepSeek API (OpenAI 兼容格式)
# 请在终端设置环境变量: export DEEPSEEK_API_KEY='your-deepseek-api-key'
API_KEY = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

# DeepSeek 官方 API 基础地址
API_BASE_URL = "https://api.deepseek.com/v1/chat/completions"
# 默认使用 DeepSeek 聊天模型 (或者 deepseek-reasoner)
DEFAULT_MODEL = "deepseek-chat"

# 简单的 ANSI 颜色输出
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

class ClaudeBotEngine:
    def __init__(self):
        self.model = DEFAULT_MODEL
        self.api_key = API_KEY

    def _call_api(self, messages: list) -> Optional[str]:
        """内部方法：调用兼容 OpenAI 格式的 DeepSeek REST API"""
        if not self.api_key:
            print(f"{RED}[Error] 未找到 API Key，请设置 DEEPSEEK_API_KEY 环境变量。{RESET}")
            return None

        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.5,
                "stream": False
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            req = urllib.request.Request(
                API_BASE_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )

            print(f"{BLUE}[Info] 正在调用 DeepSeek API (模型: {self.model})...{RESET}")
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                # 兼容 OpenAI / DeepSeek 的返回结构
                return response_data['choices'][0]['message']['content']

        except Exception as e:
            print(f"{RED}[API Error] {e}{RESET}")
            return None

    def chat(self, user_input: str):
        """交互模式：自然语言对话"""
        messages = [
            {"role": "system", "content": "You are Claude Local Bot v3.5, powered by DeepSeek backend engine."},
            {"role": "user", "content": user_input}
        ]

        response = self._call_api(messages)
        if response:
            print(f"\n{GREEN}--- DeepSeek / Bot 回复 ---{RESET}")
            print(response)
            print(f"{GREEN}--------------------------{RESET}")

    def analyze_code_file(self, file_path: str):
        """分析模式：对指定代码文件进行静态分析并交给模型审查"""
        if not os.path.exists(file_path):
            print(f"{RED}[Error] 文件不存在: {file_path}{RESET}")
            return

        print(f"\n{BLUE}[Engine] 正在启动代码分析引擎... 文件: {file_path}{RESET}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()

            lines = code_content.splitlines()
            total_lines = len(lines)
            todos = [line.strip() for line in lines if "TODO" in line]
            prints = [line.strip() for line in lines if "print(" in line and "#" not in line]

            analysis_report = {
                "file": file_path,
                "total_lines": total_lines,
                "todo_count": len(todos),
                "debug_print_count": len(prints),
                "status": "OK (Prototype Scan)"
            }

            print(f"{GREEN}--- 代码静态分析报告 ---{RESET}")
            print(json.dumps(analysis_report, indent=2, ensure_ascii=False))
            print(f"{GREEN}------------------------{RESET}")

            # 自动发送给 DeepSeek 进行深度审查
            confirm = input("是否需要发送给 DeepSeek 进行深度代码安全与逻辑审查？(y/n): ")
            if confirm.lower() == 'y':
                prompt = f"请作为代码专家，分析以下代码的潜在问题、安全隐患并给出优化后的完整代码：\n\n```python\n{code_content}\n```"
                self.chat(prompt)

        except Exception as e:
            print(f"{RED}[Analysis Error] {e}{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Claude Local Bot v3.5 (DeepSeek Edition) CLI")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # chat 子命令
    chat_parser = subparsers.add_parser("chat", help="Start interactive chat")
    chat_parser.add_argument("prompt", nargs="?", help="The message to send")

    # analyze 子命令
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a code file")
    analyze_parser.add_argument("file", help="Path to the code file")

    args = parser.parse_args()
    bot = ClaudeBotEngine()

    if args.command == "chat":
        if args.prompt:
            bot.chat(args.prompt)
        else:
            print("--- Claude Local Bot v3.5 (DeepSeek 驱动 - 交互模式) ---")
            print("输入 'exit' 或 'quit' 退出。")
            while True:
                try:
                    user_input = input("\n你: ")
                    if user_input.lower() in ['exit', 'quit']:
                        break
                    if not user_input.strip():
                        continue
                    bot.chat(user_input)
                except KeyboardInterrupt:
                    print("\n再见!")
                    break

    elif args.command == "analyze":
        bot.analyze_code_file(args.file)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
