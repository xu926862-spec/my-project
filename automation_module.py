#!/usr/bin/env python3
"""
Claude Bot v3.5 - Windows/Cross-Platform Automation Module
Provides GUI automation, screenshot, and system command execution.
"""

import os
import sys
import platform
import subprocess
from typing import Optional, Tuple

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

from rich.console import Console

console = Console()


class CrossPlatformAutomationMixin:
    """Cross-platform automation mixin for Windows/Mac/Linux"""

    def __init__(self):
        self.platform = platform.system()
        self._safety_enabled = True

        # Enable PyAutoGUI safety (moving mouse to top-left exits)
        if PYAUTOGUI_AVAILABLE:
            pyautogui.FAILSAFE = True

    def execute_system_command(self, cmd: str) -> str:
        """Execute system command (PowerShell/Bash) and return output"""
        try:
            if self.platform == "Windows":
                console.print(f"[bold cyan][Windows Command] Executing: {cmd}[/bold cyan]")
                result = subprocess.run(
                    ["powershell", "-Command", cmd],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                console.print(f"[bold cyan][Unix Command] Executing: {cmd}[/bold cyan]")
                result = subprocess.run(
                    ["bash", "-c", cmd],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

            if result.returncode == 0:
                console.print("[bold green]✓ Command executed successfully[/bold green]")
                return result.stdout.strip()
            else:
                console.print(f"[bold red]✗ Command error: {result.stderr}[/bold red]")
                return f"Error: {result.stderr.strip()}"

        except Exception as e:
            console.print(f"[bold red]✗ Execution error: {e}[/bold red]")
            return f"Exception: {str(e)}"

    def take_screenshot(self, save_path: str = "screenshot.png") -> str:
        """Take screenshot (requires PyAutoGUI)"""
        if not PYAUTOGUI_AVAILABLE:
            console.print("[bold yellow]⚠ PyAutoGUI not installed, cannot take screenshot[/bold yellow]")
            return "PyAutoGUI not available"

        if self.platform not in ["Windows", "Darwin"]:
            console.print("[bold yellow]⚠ Screenshot only supported on Windows/Mac[/bold yellow]")
            return "Screenshot not supported on this platform"

        try:
            pyautogui.screenshot(save_path)
            console.print(f"[bold green]✓ Screenshot saved:[/bold green] {save_path}")
            return f"Screenshot saved to {save_path}"
        except Exception as e:
            console.print(f"[bold red]✗ Screenshot error: {e}[/bold red]")
            return f"Error: {str(e)}"

    def gui_click(self, x: int, y: int) -> str:
        """Simulate mouse click at coordinates"""
        if not PYAUTOGUI_AVAILABLE:
            return "PyAutoGUI not available"

        if not self._safety_enabled:
            return "Safety disabled - cannot execute"

        try:
            console.print(f"[bold cyan]🖱️  Clicking at ({x}, {y})...[/bold cyan]")
            pyautogui.click(x, y)
            console.print(f"[bold green]✓ Clicked at ({x}, {y})[/bold green]")
            return f"Clicked at ({x}, {y})"
        except Exception as e:
            console.print(f"[bold red]✗ Click error: {e}[/bold red]")
            return f"Error: {str(e)}"

    def gui_type(self, text: str, interval: float = 0.05) -> str:
        """Simulate keyboard typing"""
        if not PYAUTOGUI_AVAILABLE:
            return "PyAutoGUI not available"

        if not self._safety_enabled:
            return "Safety disabled - cannot execute"

        try:
            console.print(f"[bold cyan]⌨️  Typing: {text}[/bold cyan]")
            pyautogui.write(text, interval=interval)
            console.print(f"[bold green]✓ Typed text[/bold green]")
            return f"Typed: {text}"
        except Exception as e:
            console.print(f"[bold red]✗ Type error: {e}[/bold red]")
            return f"Error: {str(e)}"

    def gui_hotkey(self, *keys: str) -> str:
        """Simulate keyboard hotkey (e.g., 'ctrl', 'c')"""
        if not PYAUTOGUI_AVAILABLE:
            return "PyAutoGUI not available"

        if not self._safety_enabled:
            return "Safety disabled - cannot execute"

        try:
            key_str = " + ".join(keys)
            console.print(f"[bold cyan]⌨️  Hotkey: {key_str}[/bold cyan]")
            pyautogui.hotkey(*keys)
            console.print(f"[bold green]✓ Hotkey executed[/bold green]")
            return f"Hotkey: {key_str}"
        except Exception as e:
            console.print(f"[bold red]✗ Hotkey error: {e}[/bold red]")
            return f"Error: {str(e)}"

    def gui_moveto(self, x: int, y: int, duration: float = 1.0) -> str:
        """Move mouse to coordinates"""
        if not PYAUTOGUI_AVAILABLE:
            return "PyAutoGUI not available"

        try:
            console.print(f"[bold cyan]🖱️  Moving to ({x}, {y})...[/bold cyan]")
            pyautogui.moveTo(x, y, duration=duration)
            console.print(f"[bold green]✓ Moved to ({x}, {y})[/bold green]")
            return f"Moved to ({x}, {y})"
        except Exception as e:
            console.print(f"[bold red]✗ Move error: {e}[/bold red]")
            return f"Error: {str(e)}"

    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position"""
        if not PYAUTOGUI_AVAILABLE:
            return (0, 0)

        try:
            x, y = pyautogui.position()
            console.print(f"[bold cyan]🖱️  Current position:[/bold cyan] ({x}, {y})")
            return (x, y)
        except Exception as e:
            console.print(f"[bold red]✗ Position error: {e}[/bold red]")
            return (0, 0)

    def disable_safety(self):
        """Disable failsafe (DANGEROUS - use with caution!)"""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.FAILSAFE = False
            self._safety_enabled = False
            console.print("[bold red]⚠️  SAFETY DISABLED - Be careful![/bold red]")

    def enable_safety(self):
        """Enable failsafe (SAFE - move mouse to top-left to exit)"""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.FAILSAFE = True
            self._safety_enabled = True
            console.print("[bold green]✓ Safety enabled (move to top-left to exit)[/bold green]")

    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen resolution"""
        if not PYAUTOGUI_AVAILABLE:
            return (0, 0)

        try:
            width, height = pyautogui.size()
            console.print(f"[bold cyan]📺 Screen size:[/bold cyan] {width}x{height}")
            return (width, height)
        except Exception as e:
            console.print(f"[bold red]✗ Size error: {e}[/bold red]")
            return (0, 0)


class WindowsSpecificAutomation(CrossPlatformAutomationMixin):
    """Windows-specific automation (inherits from cross-platform base)"""

    def open_file(self, file_path: str) -> str:
        """Open file with default application (Windows)"""
        if self.platform != "Windows":
            console.print("[bold yellow]⚠ This command works only on Windows[/bold yellow]")
            return "Windows only"

        try:
            console.print(f"[bold cyan]📂 Opening file: {file_path}[/bold cyan]")
            os.startfile(file_path)
            return f"Opened: {file_path}"
        except Exception as e:
            return f"Error: {str(e)}"

    def run_batch_script(self, batch_file: str) -> str:
        """Run a batch script"""
        if self.platform != "Windows":
            console.print("[bold yellow]⚠ Batch files only work on Windows[/bold yellow]")
            return "Windows only"

        try:
            result = subprocess.run(
                [batch_file],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def get_system_info(self) -> str:
        """Get system information"""
        if self.platform == "Windows":
            cmd = "systeminfo"
        else:
            cmd = "uname -a"

        return self.execute_system_command(cmd)


# Example usage
if __name__ == "__main__":
    bot = WindowsSpecificAutomation()

    console.print("[bold cyan]Cross-Platform Automation Module Test[/bold cyan]\n")

    # Test 1: System info
    console.print("[bold green]Test 1: System Information[/bold green]")
    print(bot.get_system_info())

    # Test 2: Screen size
    console.print("\n[bold green]Test 2: Screen Size[/bold green]")
    width, height = bot.get_screen_size()
    print(f"Screen: {width}x{height}")

    # Test 3: Execute command
    console.print("\n[bold green]Test 3: Execute Command[/bold green]")
    if bot.platform == "Windows":
        result = bot.execute_system_command("echo Hello from PowerShell")
    else:
        result = bot.execute_system_command("echo Hello from Bash")
    print(result)

    console.print("\n[bold green]✓ All tests completed[/bold green]")
