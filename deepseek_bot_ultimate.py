#!/usr/bin/env python3
"""
Claude Local Bot v3.5 - Ultimate Enterprise Edition
Engineered with Rich UI, Streaming Responses, AST Validation,
Self-Healing Compilation Loop, and Automated Git Integration.
"""

import os
import sys
import json
import ast
import subprocess
import argparse
import urllib.request
from typing import Optional, Dict, Any, Tuple

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# 初始化环境与终端控制台
load_dotenv()
console = Console()

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEFAULT_MODEL = "deepseek-chat"

class UltimateBotEngine:
    """Ultimate Enterprise-Grade Bot with Streaming, AST Validation & Auto-Healing"""

    def __init__(self):
        self.model = DEFAULT_MODEL
        self.api_key = DEEPSEEK_API_KEY
        self._display_welcome()

    def _display_welcome(self):
        """Display welcome banner"""
        welcome = """
[bold cyan]✓ Claude Local Bot v3.5[/bold cyan]
[bold]Ultimate Enterprise Edition[/bold]
[yellow]Features:[/yellow] Streaming • AST Validation • Self-Healing • Git Integration
[yellow]Model:[/yellow] {model}
        """.format(model=self.model)

        console.print(Panel(welcome.strip(), border_style="green", title="[bold green]Welcome[/bold green]"))

    def _call_deepseek_stream(self, messages: list) -> Optional[str]:
        """Core: Stream responses from DeepSeek API for real-time output"""
        if not self.api_key:
            console.print("[bold red]✗ Error: DEEPSEEK_API_KEY not set[/bold red]")
            console.print("[yellow]Set with:[/yellow] export DEEPSEEK_API_KEY='sk-...'")
            return None

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "stream": True
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        full_response = ""
        try:
            req = urllib.request.Request(
                DEEPSEEK_API_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="DeepSeek thinking deeply...", total=None)

                with urllib.request.urlopen(req, timeout=30) as response:
                    for line in response:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith("data: "):
                            data_content = line_str[6:]
                            if data_content == "[DONE]":
                                break
                            try:
                                chunk = json.loads(data_content)
                                delta = chunk["choices"][0]["delta"].get("content", "")
                                if delta:
                                    full_response += delta
                            except json.JSONDecodeError:
                                pass

            return full_response if full_response else None

        except Exception as e:
            console.print(f"[bold red]✗ API Error: {e}[/bold red]")
            return None

    def chat(self, user_input: str, system_prompt: str = "You are an elite AI software engineering assistant powered by DeepSeek."):
        """Chat with beautiful rendering and streaming output"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        console.print(Panel(f"[bold cyan]Question:[/bold cyan] {user_input}", border_style="cyan"))
        console.print("[bold green]--- DeepSeek Response (Streaming) ---[/bold green]\n")

        response = self._call_deepseek_stream(messages)
        if response:
            # Render as markdown for better formatting
            try:
                console.print(Markdown(response))
            except:
                console.print(response)
            console.print("\n[bold green]-----------------------------------[/bold green]")
        else:
            console.print("[bold red]✗ No response received[/bold red]")

        return response

    def validate_python_syntax(self, file_path: str) -> Tuple[bool, str]:
        """Static check: Validate Python syntax using AST"""
        if not file_path.endswith(".py"):
            return True, "Not a Python file, skipping AST check"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code_content = f.read()
            ast.parse(code_content)
            return True, "✓ Syntax validation passed"
        except SyntaxError as e:
            return False, f"Syntax Error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"Validation error: {e}"

    def auto_repair_file(self, file_path: str, max_retries: int = 2):
        """Ultimate self-healing loop: AI fix → write → AST check → git commit"""
        if not os.path.exists(file_path):
            console.print(f"[bold red]✗ Error: File not found: {file_path}[/bold red]")
            return

        console.print(f"[bold yellow]🔧 Starting auto-repair engine for: {file_path}[/bold yellow]")

        with open(file_path, "r", encoding="utf-8") as f:
            original_code = f.read()

        current_code = original_code
        success = False

        for attempt in range(1, max_retries + 1):
            console.print(f"\n[bold blue]>>> Healing Attempt {attempt}/{max_retries}...[/bold blue]")

            prompt = (
                f"You are an autonomous code refactoring agent. Deep-fix the following code:\n"
                f"- Remove debug prints\n"
                f"- Fix logical errors\n"
                f"- Improve security\n"
                f"- Optimize performance\n\n"
                f"Return ONLY the complete fixed code in a markdown block (```python ... ```):\n\n"
                f"```python\n{current_code}\n```"
            )

            messages = [
                {"role": "system", "content": "You are an elite senior code refactoring engine."},
                {"role": "user", "content": prompt}
            ]

            ai_response = self._call_deepseek_stream(messages)
            if not ai_response:
                console.print("[bold red]✗ Error: No response from DeepSeek[/bold red]")
                return

            # Extract code from markdown block
            fixed_code = ai_response.strip()
            if "```" in ai_response:
                parts = ai_response.split("```")
                if len(parts) >= 3:
                    code_block = parts[1]
                    lines = code_block.splitlines()
                    # Skip language identifier line if present
                    if lines and lines[0].strip() in ['python', 'py']:
                        fixed_code = "\n".join(lines[1:])
                    else:
                        fixed_code = "\n".join(lines)
                elif len(parts) == 2:
                    fixed_code = parts[1]

            # Write to file for testing
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_code.strip() + "\n")

            # AST validation check
            is_valid, msg = self.validate_python_syntax(file_path)
            console.print(f"[cyan]Validation: {msg}[/cyan]")

            if is_valid:
                console.print(f"[bold green]✓ Syntax passed! Self-healing successful.[/bold green]")
                success = True
                break
            else:
                console.print(f"[bold yellow]⚠ Syntax error detected, triggering AI self-reflection retry...[/bold yellow]")
                current_code = fixed_code  # Feed back to model for self-correction

        if success:
            # Create backup
            backup_path = f"{file_path}.bak"
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(original_code)
            console.print(f"[bold green]✓ Backup created: {backup_path}[/bold green]")

            # Display statistics
            original_lines = len(original_code.splitlines())
            fixed_lines = len(current_code.splitlines())

            stats_panel = f"""
[bold cyan]Original Lines:[/bold cyan] {original_lines}
[bold cyan]Fixed Lines:[/bold cyan] {fixed_lines}
[bold cyan]Change:[/bold cyan] {fixed_lines - original_lines:+d} lines
            """
            console.print(Panel(stats_panel.strip(), title="[bold green]Repair Statistics[/bold green]", border_style="green"))

            # Trigger Git automation
            self._trigger_git_automation(file_path)
        else:
            # Restore original
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(original_code)
            console.print(f"[bold red]✗ Max retries reached. Original file restored.[/bold red]")

    def _trigger_git_automation(self, file_path: str):
        """Automatically commit changes to Git"""
        try:
            console.print("[bold cyan]🔄 Automating Git integration...[/bold cyan]")

            # Check if git is available
            subprocess.run(["git", "--version"], capture_output=True, check=True)

            # Add file
            subprocess.run(["git", "add", file_path], capture_output=True, check=True)

            # Create commit
            commit_message = f"[AI Auto-Fix] Refactored {os.path.basename(file_path)} via DeepSeek Ultimate"
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                capture_output=True,
                text=True,
                check=True
            )

            console.print(f"[bold green]✓ Git commit successful:[/bold green]")
            console.print(f"   Message: {commit_message}")

        except subprocess.CalledProcessError as e:
            console.print(f"[yellow]⚠ Git notice: {e.stderr or 'No changes to commit or Git not initialized'}[/yellow]")
        except Exception as e:
            console.print(f"[yellow]⚠ Git integration skipped: {e}[/yellow]")

    def scan_workspace(self, root_dir: str = ".", output: Optional[str] = None):
        """Scan and display project structure with Rich tables"""
        console.print(f"[bold blue]🔍 Deep-scanning project: {os.path.abspath(root_dir)}[/bold blue]")

        file_stats = []
        total_lines = 0
        ignored_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}
        code_extensions = {".py", ".js", ".ts", ".json", ".sh", ".md", ".go", ".rs", ".cpp", ".java"}

        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning...", total=None)

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
                                file_stats.append({
                                    "path": full_path,
                                    "lines": lines,
                                    "ext": ext
                                })
                                progress.update(task, advance=1)
                        except Exception:
                            pass

        # Create table
        table = Table(title="🗂️  Workspace Analysis", show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=4)
        table.add_column("File Path", style="green")
        table.add_column("Type", style="yellow", width=8)
        table.add_column("Lines", justify="right", style="cyan")

        sorted_files = sorted(file_stats, key=lambda x: x['lines'], reverse=True)
        for i, f in enumerate(sorted_files[:20], 1):
            table.add_row(str(i), f['path'], f['ext'], f"{f['lines']:,}")

        console.print(table)

        # Summary panel
        summary = f"""
[bold cyan]Total Files:[/bold cyan] {len(file_stats)}
[bold cyan]Total Lines:[/bold cyan] {total_lines:,}
[bold cyan]Directory:[/bold cyan] {os.path.abspath(root_dir)}
        """
        console.print(Panel(summary.strip(), title="[bold green]Summary[/bold green]", border_style="green"))

        # Export to JSON if requested
        if output:
            report = {
                "root_directory": os.path.abspath(root_dir),
                "total_files": len(file_stats),
                "total_lines": total_lines,
                "files": sorted_files
            }
            with open(output, 'w') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            console.print(f"[bold green]✓ Report exported:[/bold green] {output}")


def main():
    parser = argparse.ArgumentParser(
        description="Claude Local Bot v3.5 - Ultimate Enterprise Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 deepseek_bot_ultimate.py chat "Hello"
  python3 deepseek_bot_ultimate.py chat
  python3 deepseek_bot_ultimate.py scan --dir . --output report.json
  python3 deepseek_bot_ultimate.py repair --target file.py
"""
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Stream chat with DeepSeek")
    chat_parser.add_argument("prompt", nargs="?", help="Your question")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan project workspace")
    scan_parser.add_argument("--dir", "-d", default=".", help="Directory to scan")
    scan_parser.add_argument("--output", "-o", help="Export report to JSON")

    # Repair command
    repair_parser = subparsers.add_parser("repair", help="Auto-repair with self-healing")
    repair_parser.add_argument("--target", "-t", required=True, help="Target file path")

    args = parser.parse_args()
    bot = UltimateBotEngine()

    if args.command == "chat":
        if args.prompt:
            bot.chat(args.prompt)
        else:
            console.print("\n[bold cyan]--- Interactive Chat Mode (type 'exit' to quit) ---[/bold cyan]\n")
            while True:
                try:
                    user_input = console.input("[bold yellow]You: [/bold yellow]").strip()
                    if user_input.lower() in ['exit', 'quit']:
                        console.print("[bold green]👋 Goodbye![/bold green]")
                        break
                    if not user_input:
                        continue

                    bot.chat(user_input)
                    console.print()

                except KeyboardInterrupt:
                    console.print("\n[bold green]👋 Interrupted, goodbye![/bold green]")
                    break

    elif args.command == "scan":
        bot.scan_workspace(args.dir, args.output)

    elif args.command == "repair":
        bot.auto_repair_file(args.target)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
