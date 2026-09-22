#!/usr/bin/env python3
"""
Claude Local Bot v3.5 (DeepSeek 3.5 Integration) - Production Ready
Focus: CLI Interaction, DeepSeek 3.5/OpenAI Compatible API, Advanced Code Analysis
Latest DeepSeek Models: deepseek-chat, deepseek-reasoner-1215, deepseek-coder-67b
"""

import os
import sys
import json
import argparse
import urllib.request
from typing import Optional

# --- 配置区域 (DeepSeek 3.5) ---
# 设置环境变量: export DEEPSEEK_API_KEY='your-deepseek-api-key'
API_KEY = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

# DeepSeek 官方 API 基础地址 (支持 OpenAI 兼容格式)
API_BASE_URL = "https://api.deepseek.com/v1/chat/completions"

# 可用模型列表
AVAILABLE_MODELS = {
    "chat": "deepseek-chat",                    # 标准聊天模型
    "reasoner": "deepseek-reasoner-1215",       # 推理模型 (DeepSeek 3.5最新)
    "coder": "deepseek-coder-67b",              # 代码专家
}

DEFAULT_MODEL = "deepseek-chat"  # 默认使用标准聊天

# ANSI 颜色输出
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

class ClaudeBotEngine:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model if model in AVAILABLE_MODELS.values() else DEFAULT_MODEL
        self.api_key = API_KEY
        self.request_count = 0
        print(f"{GREEN}✓ Claude Bot v3.5 (DeepSeek 3.5 后端){RESET}")
        print(f"{BLUE}   模型: {self.model}{RESET}")

    def _call_api(self, messages: list, temperature: float = 0.5) -> Optional[str]:
        """调用 DeepSeek 3.5 REST API (OpenAI 兼容格式)"""
        if not self.api_key:
            print(f"{RED}[Error] 未找到 API Key{RESET}")
            print(f"{YELLOW}请设置: export DEEPSEEK_API_KEY='your-key'{RESET}")
            return None

        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "stream": False,
                "top_p": 0.95,
                "frequency_penalty": 0,
                "presence_penalty": 0,
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

            self.request_count += 1
            print(f"{BLUE}[Request #{self.request_count}] 调用 DeepSeek 3.5 ({self.model})...{RESET}")

            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                # 兼容 OpenAI / DeepSeek 响应格式
                content = response_data['choices'][0]['message']['content']

                # 显示使用统计 (如果包含)
                if 'usage' in response_data:
                    usage = response_data['usage']
                    print(f"{GREEN}[Stats] Input: {usage.get('prompt_tokens', 0)}, "
                          f"Output: {usage.get('completion_tokens', 0)}{RESET}")

                return content

        except urllib.error.HTTPError as e:
            print(f"{RED}[API Error] HTTP {e.code}: {e.reason}{RESET}")
            return None
        except Exception as e:
            print(f"{RED}[API Error] {e}{RESET}")
            return None

    def chat(self, user_input: str, system_prompt: Optional[str] = None):
        """聊天模式 - 支持自定义系统提示"""
        if not system_prompt:
            system_prompt = "你是 Claude Local Bot v3.5，由 DeepSeek 3.5 后端驱动。你是一个有帮助的 AI 助手。"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        response = self._call_api(messages)
        if response:
            print(f"\n{GREEN}--- DeepSeek 3.5 回复 ---{RESET}")
            print(response)
            print(f"{GREEN}------------------------{RESET}\n")
            return response
        return None

    def analyze_code_file(self, file_path: str, detailed: bool = True):
        """代码分析 - 支持 DeepSeek 深度审查"""
        if not os.path.exists(file_path):
            print(f"{RED}[Error] 文件不存在: {file_path}{RESET}")
            return

        print(f"\n{BLUE}[Engine] 启动代码分析引擎 (文件: {file_path}){RESET}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()

            # 基础静态分析
            lines = code_content.splitlines()
            total_lines = len(lines)
            todos = [line.strip() for line in lines if "TODO" in line or "FIXME" in line]
            prints = [line.strip() for line in lines if "print(" in line and "#" not in line]
            imports = [line.strip() for line in lines if "import" in line]

            # 构建分析报告
            analysis_report = {
                "file": file_path,
                "total_lines": total_lines,
                "import_count": len(imports),
                "todo_count": len(todos),
                "debug_print_count": len(prints),
                "status": "✓ 分析完成"
            }

            print(f"\n{GREEN}--- 代码静态分析报告 ---{RESET}")
            print(json.dumps(analysis_report, indent=2, ensure_ascii=False))
            print(f"{GREEN}------------------------{RESET}\n")

            # 询问是否进行深度 DeepSeek 审查
            if detailed:
                try:
                    confirm = input("是否发送给 DeepSeek 3.5 进行深度分析？(y/n): ").strip().lower()
                    if confirm == 'y':
                        prompt = (
                            f"请作为资深代码审查专家，使用 DeepSeek 3.5 推理能力分析以下代码：\n\n"
                            f"1. 识别所有潜在的代码缺陷和安全隐患\n"
                            f"2. 评估代码质量和复杂度\n"
                            f"3. 提出优化建议\n"
                            f"4. 给出改进后的完整代码\n\n"
                            f"```python\n{code_content}\n```"
                        )
                        self.chat(prompt, system_prompt="你是一个专业的代码审查专家，使用 DeepSeek 3.5 的推理能力进行深度分析。")
                except EOFError:
                    print(f"{YELLOW}[Info] 跳过交互式确认{RESET}")

        except Exception as e:
            print(f"{RED}[Analysis Error] {e}{RESET}")

    def list_models(self):
        """列出可用模型"""
        print(f"\n{GREEN}--- 可用模型列表 ---{RESET}")
        for alias, model in AVAILABLE_MODELS.items():
            marker = "✓" if model == self.model else " "
            print(f"  [{marker}] {alias:12} -> {model}")
        print(f"{GREEN}-------------------{RESET}\n")

def main():
    parser = argparse.ArgumentParser(
        description="Claude Local Bot v3.5 (DeepSeek 3.5) CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # chat 子命令
    chat_parser = subparsers.add_parser("chat", help="交互式聊天")
    chat_parser.add_argument("prompt", nargs="?", help="要发送的消息")
    chat_parser.add_argument("--model", choices=list(AVAILABLE_MODELS.keys()),
                           help="使用的模型")
    chat_parser.add_argument("--system", help="自定义系统提示")

    # analyze 子命令
    analyze_parser = subparsers.add_parser("analyze", help="代码分析")
    analyze_parser.add_argument("file", help="代码文件路径")
    analyze_parser.add_argument("--model", choices=list(AVAILABLE_MODELS.keys()),
                              default="reasoner", help="分析使用的模型")
    analyze_parser.add_argument("--no-review", action="store_true",
                              help="跳过 DeepSeek 深度审查")

    # models 子命令
    models_parser = subparsers.add_parser("models", help="列出可用模型")

    args = parser.parse_args()

    # 获取模型
    model = DEFAULT_MODEL
    if hasattr(args, 'model') and args.model:
        model = AVAILABLE_MODELS.get(args.model, DEFAULT_MODEL)

    # 初始化引擎
    bot = ClaudeBotEngine(model)

    if args.command == "chat":
        if args.prompt:
            bot.chat(args.prompt, system_prompt=args.system if hasattr(args, 'system') else None)
        else:
            print(f"\n{YELLOW}--- Claude Local Bot v3.5 (DeepSeek 驱动 - 交互模式) ---{RESET}")
            print("输入 'exit' 或 'quit' 退出，'models' 查看模型列表\n")
            while True:
                try:
                    user_input = input(f"{BLUE}你:{RESET} ").strip()
                    if user_input.lower() in ['exit', 'quit']:
                        print(f"{GREEN}👋 再见！{RESET}")
                        break
                    elif user_input.lower() == 'models':
                        bot.list_models()
                        continue
                    if not user_input:
                        continue
                    bot.chat(user_input)
                except KeyboardInterrupt:
                    print(f"\n{GREEN}👋 再见！{RESET}")
                    break
                except EOFError:
                    break

    elif args.command == "analyze":
        detailed = not getattr(args, 'no_review', False)
        bot.analyze_code_file(args.file, detailed=detailed)

    elif args.command == "models":
        bot.list_models()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
