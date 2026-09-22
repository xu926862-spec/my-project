#!/usr/bin/env python3
"""
Claude Local Bot v3.5 - Enhanced Edition with Rich UI
Powered by: DeepSeek API + Rich Terminal + python-dotenv
"""

import os
import sys
import json
import argparse
import urllib.request
from typing import Optional, Dict, Any
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.syntax import Syntax
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = os.environ.get("API_BASE_URL", "https://api.deepseek.com/v1/chat/completions")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "deepseek-chat")
API_TIMEOUT = int(os.environ.get("API_TIMEOUT", "30"))

# Rich console for beautiful output
console = Console()

class EnhancedDeepSeekBot:
    """Enhanced DeepSeek Bot with Rich terminal UI"""

    def __init__(self):
        self.model = DEFAULT_MODEL
        self.api_key = DEEPSEEK_API_KEY
        self.request_count = 0

        # Display welcome message
        welcome_panel = Panel(
            "[bold cyan]✓ DeepSeek Bot v3.5 (Enhanced Edition)[/bold cyan]\n"
            f"[yellow]Model:[/yellow] {self.model}\n"
            f"[yellow]Status:[/yellow] Ready",
            title="[bold]Welcome[/bold]",
            border_style="green"
        )
        console.print(welcome_panel)

    def _call_deepseek(self, messages: list) -> Optional[str]:
        """Call DeepSeek API with error handling"""
        if not self.api_key:
            console.print("[bold red]✗ Error:[/bold red] DEEPSEEK_API_KEY not set")
            console.print("[yellow]Set it with:[/yellow] export DEEPSEEK_API_KEY='sk-...'")
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

            self.request_count += 1
            with console.status(f"[cyan]Calling DeepSeek API (Model: {self.model})..."):
                with urllib.request.urlopen(req, timeout=API_TIMEOUT) as response:
                    response_data = json.loads(response.read().decode('utf-8'))
                    return response_data['choices'][0]['message']['content']

        except Exception as e:
            console.print(f"[bold red]✗ API Error:[/bold red] {e}")
            return None

    def chat(self, user_input: str) -> Optional[str]:
        """Chat with DeepSeek"""
        messages = [
            {"role": "system", "content": "You are an expert AI software engineer powered by DeepSeek."},
            {"role": "user", "content": user_input}
        ]
        return self._call_deepseek(messages)

    def scan_workspace(self, root_dir: str = ".") -> Dict[str, Any]:
        """Scan project workspace with progress indicator"""
        console.print(f"\n[cyan]Scanning:[/cyan] {Path(root_dir).absolute()}")

        file_stats = []
        total_lines = 0
        ignored_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}
        code_extensions = {".py", ".js", ".ts", ".json", ".sh", ".md", ".go", ".rs"}

        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning files...", total=None)

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

        return {
            "root_directory": str(Path(root_dir).absolute()),
            "total_files": len(file_stats),
            "total_lines": total_lines,
            "files": sorted(file_stats, key=lambda x: x['lines'], reverse=True)
        }

    def display_scan_report(self, report: Dict[str, Any], limit: int = 10):
        """Display scan report with rich formatting"""
        # Create summary panel
        summary = f"""
[bold]Directory:[/bold] {report['root_directory']}
[bold]Total Files:[/bold] {report['total_files']}
[bold]Total Lines:[/bold] [cyan]{report['total_lines']:,}[/cyan]
        """

        console.print(Panel(summary.strip(), title="[bold green]Scan Report[/bold green]", border_style="green"))

        # Create table for files
        table = Table(title="Largest Files", show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("File", style="green")
        table.add_column("Lines", justify="right", style="yellow")

        for i, f in enumerate(report['files'][:limit], 1):
            lines_str = f"{f['lines']:,}"
            table.add_row(str(i), f['path'], lines_str)

        console.print(table)

    def auto_repair_file(self, file_path: str):
        """Auto repair file with progress indicator"""
        if not Path(file_path).exists():
            console.print(f"[bold red]✗ Error:[/bold red] File not found: {file_path}")
            return

        console.print(f"\n[cyan]Analyzing:[/cyan] {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_code = f.read()

            file_ext = Path(file_path).suffix[1:] or "python"

            prompt = (
                f"Fix the following {file_ext} code. Remove debug prints, "
                f"fix bugs, and improve security. Return only the fixed code in a markdown block.\n\n"
                f"```{file_ext}\n{original_code}\n```"
            )

            with console.status("[cyan]Getting AI-powered optimization..."):
                ai_response = self.chat(prompt)

            if not ai_response:
                return

            # Extract code from markdown
            fixed_code = ai_response.strip()
            if "```" in ai_response:
                parts = ai_response.split("```")
                if len(parts) >= 3:
                    code_block = parts[1]
                    lines = code_block.split('\n')
                    if lines and lines[0].strip() in [file_ext, 'python', 'javascript']:
                        fixed_code = '\n'.join(lines[1:])
                    else:
                        fixed_code = code_block

            # Create backup
            backup_path = f"{file_path}.bak"
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(original_code)

            # Write fixed code
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_code.strip() + "\n")

            # Display results
            original_lines = len(original_code.splitlines())
            fixed_lines = len(fixed_code.splitlines())

            result_panel = Panel(
                f"[green]✓ Repair Complete![/green]\n\n"
                f"[yellow]Original Lines:[/yellow] {original_lines}\n"
                f"[yellow]Fixed Lines:[/yellow] {fixed_lines}\n"
                f"[yellow]Backup:[/yellow] {backup_path}",
                title="[bold green]Success[/bold green]",
                border_style="green"
            )
            console.print(result_panel)

        except Exception as e:
            console.print(f"[bold red]✗ Repair Error:[/bold red] {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Claude Bot v3.5 (Enhanced Edition)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 deepseek_bot_enhanced.py chat "Hello"
  python3 deepseek_bot_enhanced.py scan --dir .
  python3 deepseek_bot_enhanced.py repair --target file.py
"""
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with DeepSeek")
    chat_parser.add_argument("prompt", nargs="?", help="Your message")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan workspace")
    scan_parser.add_argument("--dir", "-d", default=".", help="Directory to scan")
    scan_parser.add_argument("--output", "-o", help="Save report to JSON")
    scan_parser.add_argument("--limit", "-l", type=int, default=10, help="Show top N files")

    # Repair command
    repair_parser = subparsers.add_parser("repair", help="Auto-repair code")
    repair_parser.add_argument("--target", "-t", required=True, help="Target file")

    args = parser.parse_args()
    bot = EnhancedDeepSeekBot()

    if args.command == "chat":
        if args.prompt:
            response = bot.chat(args.prompt)
            if response:
                console.print(Panel(response, title="[bold cyan]DeepSeek Response[/bold cyan]", border_style="cyan"))
        else:
            console.print("\n[bold cyan]Interactive Chat Mode[/bold cyan]")
            console.print("[yellow]Type 'exit' or 'quit' to quit\n")

            while True:
                try:
                    user_input = console.input("[bold cyan]You:[/bold cyan] ").strip()
                    if user_input.lower() in ['exit', 'quit']:
                        console.print("[green]👋 Goodbye![/green]")
                        break
                    if not user_input:
                        continue

                    response = bot.chat(user_input)
                    if response:
                        console.print(Panel(response, border_style="cyan"))
                        console.print()

                except KeyboardInterrupt:
                    console.print("\n[green]👋 Interrupted, goodbye![/green]")
                    break

    elif args.command == "scan":
        report = bot.scan_workspace(args.dir)
        bot.display_scan_report(report, args.limit)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            console.print(f"\n[green]✓ Report saved:[/green] {args.output}")

    elif args.command == "repair":
        bot.auto_repair_file(args.target)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
