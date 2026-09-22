#!/usr/bin/env python3
"""
Claude Local Bot v3.5 (Advanced Enterprise Edition)
Features: CLI, DeepSeek/API Engine, Workspace Scanner, Auto-Repair & Write-back
"""

import os
import sys
import json
import argparse
import urllib.request
from typing import Optional, Dict, Any, List

# --- 配置区域 ---
API_KEY = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
API_BASE_URL = "https://api.deepseek.com/v1/chat/completions"
DEFAULT_MODEL = "deepseek-chat"

# 终端颜色
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

class ClaudeBotEngine:
    def __init__(self):
        self.model = DEFAULT_MODEL
        self.api_key = API_KEY
        print(f"{GREEN}✓ Claude Local Bot v3.5 (Advanced Edition) 已初始化{RESET}")
        print(f"{BLUE}  模型: {self.model}{RESET}\n")

    def _call_api(self, messages: list) -> Optional[str]:
        """调用大模型 API 核心方法"""
        if not self.api_key:
            print(f"{RED}[Error] 未找到 API Key，请设置 DEEPSEEK_API_KEY 环境变量。{RESET}")
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
                API_BASE_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )

            print(f"{BLUE}[Info] 正在请求大模型 ({self.model})...{RESET}")
            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                return response_data['choices'][0]['message']['content']

        except Exception as e:
            print(f"{RED}[API Error] {e}{RESET}")
            return None

    def chat(self, user_input: str) -> Optional[str]:
        """通用自然语言对话"""
        messages = [
            {"role": "system", "content": "You are Claude Local Bot v3.5, an elite AI software engineering assistant."},
            {"role": "user", "content": user_input}
        ]
        return self._call_api(messages)

    def scan_workspace(self, root_dir: str = ".") -> Dict[str, Any]:
        """【新增】全项目目录智能扫描引擎"""
        print(f"\n{BLUE}[Engine] 正在扫描项目目录: {os.path.abspath(root_dir)}{RESET}")
        file_stats = []
        total_lines = 0
        ignored_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build", ".pytest_cache"}
        code_extensions = {".py", ".js", ".ts", ".json", ".sh", ".md", ".go", ".rs", ".cpp", ".java", ".c", ".h"}

        file_count = 0
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # 过滤不需要扫描的目录
            dirnames[:] = [d for d in dirnames if d not in ignored_dirs]

            for file in filenames:
                full_path = os.path.join(dirpath, file)
                ext = os.path.splitext(file)[1]

                if ext in code_extensions:
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            lines = len(f.readlines())
                            total_lines += lines
                            file_stats.append({
                                "path": full_path,
                                "lines": lines,
                                "ext": ext,
                                "size_bytes": os.path.getsize(full_path)
                            })
                            file_count += 1
                    except Exception:
                        pass

        report = {
            "root_directory": os.path.abspath(root_dir),
            "total_files_scanned": file_count,
            "total_lines_of_code": total_lines,
            "files": sorted(file_stats, key=lambda x: x['lines'], reverse=True),
            "status": "✓ 扫描完成"
        }

        print(f"{GREEN}✓ 扫描完成: {file_count} 个文件, {total_lines} 行代码{RESET}\n")
        return report

    def auto_repair_file(self, file_path: str):
        """【新增】自动修复与回写引擎：分析代码 -> AI 修复 -> 自动安全写回文件"""
        if not os.path.exists(file_path):
            print(f"{RED}[Error] 目标文件不存在: {file_path}{RESET}")
            return

        print(f"\n{YELLOW}[Auto-Repair] 正在读取并分析文件: {file_path}{RESET}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_code = f.read()

            # 获取文件扩展名用于优化提示词
            file_ext = os.path.splitext(file_path)[1][1:]  # 去掉点号

            # 构造大模型修复提示词
            prompt = (
                f"你是一个自动代码修复引擎。请检查以下 {file_ext} 代码中的 Bug、安全隐患或不规范写法，"
                f"并直接给出**修复后的完整代码**。\n\n"
                f"【极其重要】：只输出纯代码内容或用标准 markdown 代码块包裹，不要夹杂过多的废话解释，"
                f"以便系统可以直接提取并写回文件。\n\n"
                f"```{file_ext}\n{original_code}\n```"
            )

            print(f"{BLUE}[Auto-Repair] 正在发送给 AI 求解优化方案...{RESET}")
            ai_response = self.chat(prompt)

            if not ai_response:
                print(f"{RED}[Error] AI 未能返回有效修复方案。{RESET}")
                return

            # 智能提取 Markdown 代码块中的内容
            fixed_code = ai_response.strip()

            if "```" in ai_response:
                parts = ai_response.split("```")
                if len(parts) >= 3:
                    # 提取第一个代码块之间的内容
                    code_block = parts[1]
                    lines = code_block.split('\n')

                    # 跳过语言标识符行（如 python, js 等）
                    if lines and lines[0].strip() in [file_ext, 'python', 'javascript', 'typescript', 'bash', 'sh', 'json']:
                        fixed_code = '\n'.join(lines[1:])
                    else:
                        fixed_code = code_block
                elif len(parts) == 2:
                    fixed_code = parts[1]

            # 备份原文件
            backup_path = f"{file_path}.bak"
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(original_code)
            print(f"{GREEN}[Backup] 已自动创建文件备份: {backup_path}{RESET}")

            # 自动写回新代码
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_code.strip() + "\n")

            # 显示修改统计
            original_lines = len(original_code.splitlines())
            fixed_lines = len(fixed_code.splitlines())
            print(f"{GREEN}[Success] 自动修复完成！{RESET}")
            print(f"  原代码行数: {original_lines}")
            print(f"  修复后行数: {fixed_lines}")
            print(f"  文件位置: {file_path}\n")

        except Exception as e:
            print(f"{RED}[Repair Error] 自动修复执行失败: {e}{RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Claude Local Bot v3.5 (Advanced Enterprise Edition)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 交互式聊天
  python3 claude_bot_advanced.py chat "你好"

  # 扫描整个项目
  python3 claude_bot_advanced.py scan --dir .

  # 自动修复文件
  python3 claude_bot_advanced.py repair --target file.py
"""
    )
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    # 1. Chat 命令
    chat_parser = subparsers.add_parser("chat", help="Interactive AI chat")
    chat_parser.add_argument("prompt", nargs="?", help="Chat prompt")
    chat_parser.add_argument("--model", help="Select model")

    # 2. Scan 命令（全项目扫描）
    scan_parser = subparsers.add_parser("scan", help="Scan entire workspace")
    scan_parser.add_argument("--dir", "-d", default=".", help="Directory to scan (default: .)")
    scan_parser.add_argument("--output", "-o", help="Save report to JSON file")

    # 3. Repair 命令（自动修复并写回文件）
    repair_parser = subparsers.add_parser("repair", help="Auto-repair and write-back code")
    repair_parser.add_argument("--target", "-t", required=True, help="Target file path")

    args = parser.parse_args()
    bot = ClaudeBotEngine()

    if args.command == "chat":
        if args.prompt:
            res = bot.chat(args.prompt)
            if res:
                print(f"\n{GREEN}--- 助手回复 ---{RESET}\n{res}\n{GREEN}----------------{RESET}\n")
        else:
            print("--- Claude Local Bot v3.5 (交互模式) ---")
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
                        print(f"\n{GREEN}--- 助手回复 ---{RESET}\n{res}\n{GREEN}----------------{RESET}\n")
                except KeyboardInterrupt:
                    print(f"\n{GREEN}👋 再见！{RESET}")
                    break

    elif args.command == "scan":
        report = bot.scan_workspace(args.dir)

        # 显示报告
        print(f"{GREEN}--- 项目扫描报告 ---{RESET}")
        print(f"目录: {report['root_directory']}")
        print(f"文件数: {report['total_files_scanned']}")
        print(f"总行数: {report['total_lines_of_code']}")
        print(f"\n前 10 个最大文件:")
        for i, f in enumerate(report['files'][:10], 1):
            print(f"  {i}. {f['path']:40} ({f['lines']:5} 行)")
        print(f"{GREEN}-------------------{RESET}\n")

        # 可选：保存到文件
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
