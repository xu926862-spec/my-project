#!/usr/bin/env python3
"""
Claude Local Bot v3.5 - DeepSeek Edition
Pure DeepSeek API Integration with Workspace Scan & Auto-Repair
"""

import os
import sys
import json
import argparse
import urllib.request
from typing import Optional, Dict, Any

# --- 配置区域 ---
# 从环境变量读取 DeepSeek API Key
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
# 默认使用 DeepSeek 聊天模型
DEFAULT_MODEL = "deepseek-chat"

# 终端颜色输出
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

class DeepSeekBotEngine:
    def __init__(self):
        self.model = DEFAULT_MODEL
        self.api_key = DEEPSEEK_API_KEY
        print(f"{GREEN}✓ DeepSeek Bot v3.5 已初始化{RESET}")
        print(f"{BLUE}  模型: {self.model}{RESET}\n")

    def _call_deepseek(self, messages: list) -> Optional[str]:
        """纯 DeepSeek API 调用核心"""
        if not self.api_key:
            print(f"{RED}[Error] 未检测到 DEEPSEEK_API_KEY{RESET}")
            print(f"{YELLOW}请先运行: export DEEPSEEK_API_KEY='sk-your-api-key'{RESET}")
            return None

        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.2,
                "stream": False
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            req = urllib.request.Request(
                DEEPSEEK_API_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )

            print(f"{BLUE}[Info] 正在请求 DeepSeek API (模型: {self.model})...{RESET}")
            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                return response_data['choices'][0]['message']['content']

        except Exception as e:
            print(f"{RED}[API Error] {e}{RESET}")
            return None

    def chat(self, user_input: str) -> Optional[str]:
        """与 DeepSeek 进行对话"""
        messages = [
            {"role": "system", "content": "You are an expert AI software engineer powered by DeepSeek."},
            {"role": "user", "content": user_input}
        ]
        return self._call_deepseek(messages)

    def scan_workspace(self, root_dir: str = ".") -> Dict[str, Any]:
        """扫描项目目录下的代码文件"""
        print(f"\n{BLUE}[Engine] 正在扫描目录: {os.path.abspath(root_dir)}{RESET}")
        file_stats = []
        total_lines = 0
        ignored_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build", ".pytest_cache"}
        code_extensions = {".py", ".js", ".ts", ".json", ".sh", ".md", ".go", ".rs", ".cpp", ".java"}

        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
            for file in filenames:
                full_path = os.path.join(dirpath, file)
                ext = os.path.splitext(file)[1]
                if ext in code_extensions:
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            lines = len(f.readlines())
                            total_lines += lines
                            file_stats.append({"path": full_path, "lines": lines, "ext": ext})
                    except Exception:
                        pass

        print(f"{GREEN}✓ 扫描完成: {len(file_stats)} 个文件, {total_lines} 行代码{RESET}\n")

        return {
            "root_directory": os.path.abspath(root_dir),
            "total_files": len(file_stats),
            "total_lines": total_lines,
            "files": sorted(file_stats, key=lambda x: x['lines'], reverse=True)
        }

    def auto_repair_file(self, file_path: str):
        """让 DeepSeek 自动修复代码并安全写回文件"""
        if not os.path.exists(file_path):
            print(f"{RED}[Error] 文件不存在: {file_path}{RESET}")
            return

        print(f"\n{YELLOW}[Auto-Repair] 正在读取并分析文件: {file_path}{RESET}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_code = f.read()

            # 获取文件类型
            file_ext = os.path.splitext(file_path)[1][1:] or "python"

            prompt = (
                f"请作为资深代码专家，修复以下 {file_ext} 代码中的错误、优化逻辑并提升性能。"
                f"请直接输出**修复后的完整代码**。务必用标准 markdown 代码块包裹，"
                f"不要输出过多废话，以便系统自动提取写回文件。\n\n"
                f"```{file_ext}\n{original_code}\n```"
            )

            print(f"{BLUE}[Auto-Repair] 正在等待 DeepSeek 返回优化方案...{RESET}")
            ai_response = self.chat(prompt)
            if not ai_response:
                return

            # 智能从 Markdown 中提取代码
            fixed_code = ai_response.strip()
            if "```" in ai_response:
                parts = ai_response.split("```")
                if len(parts) >= 3:
                    code_block = parts[1]
                    lines = code_block.split('\n')
                    # 去掉第一行的语言标识
                    if lines and lines[0].strip() in [file_ext, 'python', 'javascript', 'bash', 'sh']:
                        fixed_code = '\n'.join(lines[1:])
                    else:
                        fixed_code = code_block
                elif len(parts) == 2:
                    fixed_code = parts[1]

            # 自动备份原文件
            backup_path = f"{file_path}.bak"
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(original_code)
            print(f"{GREEN}[Backup] 已自动生成备份: {backup_path}{RESET}")

            # 自动写回修复后的代码
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_code.strip() + "\n")

            original_lines = len(original_code.splitlines())
            fixed_lines = len(fixed_code.splitlines())

            print(f"{GREEN}[Success] 修复完成！{RESET}")
            print(f"  原代码行数: {original_lines}")
            print(f"  修复后行数: {fixed_lines}")
            print(f"  文件位置: {file_path}\n")

        except Exception as e:
            print(f"{RED}[Repair Error] 修复失败: {e}{RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Claude Local Bot v3.5 (DeepSeek Edition)",
        epilog="""
使用示例:
  python3 deepseek_bot.py chat "你好"
  python3 deepseek_bot.py scan
  python3 deepseek_bot.py repair --target file.py
"""
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # chat 命令
    chat_parser = subparsers.add_parser("chat", help="Chat with DeepSeek")
    chat_parser.add_argument("prompt", nargs="?", help="Your message")

    # scan 命令
    scan_parser = subparsers.add_parser("scan", help="Scan project workspace")
    scan_parser.add_argument("--dir", "-d", default=".", help="Directory to scan")
    scan_parser.add_argument("--output", "-o", help="Save report to JSON")

    # repair 命令
    repair_parser = subparsers.add_parser("repair", help="Auto repair code file")
    repair_parser.add_argument("--target", "-t", required=True, help="Target file path")

    args = parser.parse_args()
    bot = DeepSeekBotEngine()

    if args.command == "chat":
        if args.prompt:
            res = bot.chat(args.prompt)
            if res:
                print(f"\n{GREEN}--- DeepSeek 回复 ---{RESET}\n{res}\n{GREEN}------------------{RESET}\n")
        else:
            print("--- DeepSeek Bot (交互模式) ---")
            print("输入 'exit' 或 'quit' 退出。\n")
            while True:
                try:
                    user_input = input(f"{BLUE}你:{RESET} ")
                    if user_input.lower() in ['exit', 'quit']:
                        print(f"{GREEN}👋 再见！{RESET}")
                        break
                    if not user_input.strip():
                        continue
                    res = bot.chat(user_input)
                    if res:
                        print(f"\n{GREEN}--- DeepSeek 回复 ---{RESET}\n{res}\n{GREEN}------------------{RESET}\n")
                except KeyboardInterrupt:
                    print(f"\n{GREEN}👋 再见！{RESET}")
                    break

    elif args.command == "scan":
        report = bot.scan_workspace(args.dir)
        print(f"{GREEN}--- 项目扫描报告 ---{RESET}")
        print(f"目录: {report['root_directory']}")
        print(f"文件数: {report['total_files']}")
        print(f"总行数: {report['total_lines']}")
        print(f"\n前 10 个最大文件:")
        for i, f in enumerate(report['files'][:10], 1):
            print(f"  {i}. {f['path']:45} ({f['lines']:5} 行)")
        print(f"{GREEN}-------------------{RESET}\n")

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"{GREEN}✓ 报告已保存: {args.output}{RESET}\n")

    elif args.command == "repair":
        bot.auto_repair_file(args.target)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
