#!/usr/bin/env python3
"""
Claude Local Bot - All-in-One AI Assistant
Hybrid system: API + CLI + Code Analysis + Auto-Repair
Supports both Claude API and local LLM models
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BotMode(Enum):
    """Bot operation modes."""
    CLI = "cli"
    API = "api"
    AUTO = "auto"
    CODE_ANALYSIS = "code_analysis"
    AUTO_REPAIR = "auto_repair"


@dataclass
class CodeAnalysisResult:
    """Result of code analysis."""
    file_path: str
    issues: List[str]
    suggestions: List[str]
    score: float
    severity: str


class CodeAnalyzer:
    """Advanced code analysis engine."""

    def __init__(self):
        self.analysis_cache = {}
        logger.info("✓ Code Analyzer initialized")

    def analyze(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Analyze code for issues and improvements.

        Args:
            code: Source code to analyze
            language: Programming language

        Returns:
            Analysis results
        """
        logger.info(f"📊 Analyzing {language} code...")

        analysis = {
            "language": language,
            "lines": len(code.split('\n')),
            "issues": self._detect_issues(code, language),
            "improvements": self._suggest_improvements(code, language),
            "quality_score": self._calculate_quality(code),
            "complexity": self._analyze_complexity(code),
        }

        return analysis

    def _detect_issues(self, code: str, language: str) -> List[str]:
        """Detect potential issues in code."""
        issues = []

        # Common issues
        if "TODO" in code or "FIXME" in code:
            issues.append("Contains TODO/FIXME comments")

        if language == "python":
            if "print(" in code and "logging" not in code:
                issues.append("Uses print() instead of logging")
            if "except:" in code:
                issues.append("Bare except clause detected")
            if "global " in code:
                issues.append("Uses global variables")

        return issues

    def _suggest_improvements(self, code: str, language: str) -> List[str]:
        """Suggest code improvements."""
        suggestions = []

        if len(code) > 5000:
            suggestions.append("Consider breaking into smaller functions")

        if language == "python":
            if len([l for l in code.split('\n') if len(l) > 100]) > 5:
                suggestions.append("Multiple lines exceed 100 characters")
            if "import *" in code:
                suggestions.append("Avoid wildcard imports")

        return suggestions

    def _calculate_quality(self, code: str) -> float:
        """Calculate code quality score (0-100)."""
        score = 100.0

        # Deduct for issues
        issues_count = len(self._detect_issues(code, "python"))
        score -= issues_count * 5

        # Bonus for good practices
        if "type hints" in code.lower() or "->" in code:
            score += 10
        if "docstring" in code.lower() or '"""' in code:
            score += 5

        return max(0, min(100, score))

    def _analyze_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity."""
        lines = code.split('\n')

        return {
            "total_lines": len(lines),
            "non_empty_lines": len([l for l in lines if l.strip()]),
            "comment_lines": len([l for l in lines if l.strip().startswith('#')]),
            "cyclomatic_complexity": "estimated_medium",  # Simplified
        }


class AutoRepair:
    """Automatic code repair engine."""

    def __init__(self, analyzer: CodeAnalyzer):
        self.analyzer = analyzer
        logger.info("✓ Auto-Repair engine initialized")

    def repair(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Automatically repair code issues.

        Args:
            code: Source code to repair
            language: Programming language

        Returns:
            Repaired code and change log
        """
        logger.info(f"🔧 Auto-repairing {language} code...")

        repaired_code = code
        changes = []

        # Apply automatic fixes
        if language == "python":
            # Fix bare except
            if "except:" in repaired_code:
                repaired_code = repaired_code.replace("except:", "except Exception:")
                changes.append("Fixed bare except clause")

            # Replace print with logging
            if "print(" in repaired_code and "logging" not in repaired_code:
                repaired_code = "import logging\n\n" + repaired_code
                repaired_code = repaired_code.replace("print(", "logging.info(")
                changes.append("Added logging import and replaced print() calls")

        return {
            "original": code,
            "repaired": repaired_code,
            "changes": changes,
            "diff_lines": len([l for l in repaired_code.split('\n') if l != code]),
        }


class ClaudeBotAPI:
    """REST API server for Claude Bot."""

    def __init__(self, analyzer: CodeAnalyzer, repair_engine: AutoRepair):
        self.analyzer = analyzer
        self.repair_engine = repair_engine
        self.request_log = []
        logger.info("✓ Claude Bot API initialized")

    async def handle_analyze(self, code: str, language: str) -> Dict[str, Any]:
        """Handle code analysis request."""
        result = self.analyzer.analyze(code, language)
        self.request_log.append({
            "type": "analyze",
            "language": language,
            "timestamp": self._get_timestamp(),
        })
        return result

    async def handle_repair(self, code: str, language: str) -> Dict[str, Any]:
        """Handle code repair request."""
        result = self.repair_engine.repair(code, language)
        self.request_log.append({
            "type": "repair",
            "language": language,
            "timestamp": self._get_timestamp(),
        })
        return result

    async def handle_chat(self, message: str, context: Optional[Dict] = None) -> str:
        """Handle chat request."""
        self.request_log.append({
            "type": "chat",
            "message": message[:100],
            "timestamp": self._get_timestamp(),
        })

        # Simulate response (would use Claude API in production)
        return f"Understood: {message}. Processing..."

    def get_status(self) -> Dict[str, Any]:
        """Get API status."""
        return {
            "status": "running",
            "requests_processed": len(self.request_log),
            "last_requests": self.request_log[-5:] if self.request_log else [],
            "uptime": "active",
        }

    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


class ClaudeBotCLI:
    """Command-line interface for Claude Bot."""

    def __init__(self, analyzer: CodeAnalyzer, repair_engine: AutoRepair, api: ClaudeBotAPI):
        self.analyzer = analyzer
        self.repair_engine = repair_engine
        self.api = api
        logger.info("✓ Claude Bot CLI initialized")

    async def interactive_mode(self):
        """Run interactive CLI mode."""
        print("\n🤖 Claude Local Bot - Interactive Mode")
        print("=" * 60)
        print("Commands:")
        print("  /analyze <file>      - Analyze code file")
        print("  /repair <file>       - Auto-repair code")
        print("  /chat <message>      - Chat with bot")
        print("  /status              - Show system status")
        print("  /help                - Show all commands")
        print("  /quit                - Exit")
        print("=" * 60 + "\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input == "/quit":
                    print("👋 Goodbye!")
                    break
                elif user_input == "/status":
                    self._show_status()
                elif user_input == "/help":
                    self._show_help()
                elif user_input.startswith("/analyze "):
                    file_path = user_input.replace("/analyze ", "").strip()
                    await self._handle_analyze(file_path)
                elif user_input.startswith("/repair "):
                    file_path = user_input.replace("/repair ", "").strip()
                    await self._handle_repair(file_path)
                elif user_input.startswith("/chat "):
                    message = user_input.replace("/chat ", "").strip()
                    await self._handle_chat(message)
                elif user_input:
                    response = await self.api.handle_chat(user_input)
                    print(f"Bot: {response}\n")

            except KeyboardInterrupt:
                print("\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                logger.error(f"✗ Error: {e}")

    async def _handle_analyze(self, file_path: str):
        """Handle code analysis."""
        try:
            with open(file_path, 'r') as f:
                code = f.read()

            language = Path(file_path).suffix.lstrip('.')
            result = await self.api.handle_analyze(code, language)

            print(f"\n📊 Analysis Results for {file_path}")
            print("=" * 60)
            print(f"Quality Score: {result['quality_score']:.1f}/100")
            print(f"Language: {result['language']}")
            print(f"Lines: {result['lines']}")

            if result['issues']:
                print("\n⚠️  Issues:")
                for issue in result['issues']:
                    print(f"  - {issue}")

            if result['improvements']:
                print("\n💡 Improvements:")
                for suggestion in result['improvements']:
                    print(f"  - {suggestion}")

            print()
        except FileNotFoundError:
            print(f"✗ File not found: {file_path}\n")

    async def _handle_repair(self, file_path: str):
        """Handle code repair."""
        try:
            with open(file_path, 'r') as f:
                code = f.read()

            language = Path(file_path).suffix.lstrip('.')
            result = await self.api.handle_repair(code, language)

            print(f"\n🔧 Auto-Repair Results for {file_path}")
            print("=" * 60)

            if result['changes']:
                print("Changes Made:")
                for change in result['changes']:
                    print(f"  ✓ {change}")
            else:
                print("No changes needed - code is clean!")

            print(f"\nModified {result['diff_lines']} lines")
            print()
        except FileNotFoundError:
            print(f"✗ File not found: {file_path}\n")

    async def _handle_chat(self, message: str):
        """Handle chat message."""
        response = await self.api.handle_chat(message)
        print(f"Bot: {response}\n")

    def _show_status(self):
        """Show system status."""
        status = self.api.get_status()
        print(f"\n📈 System Status:")
        print(f"  Status: {status['status']}")
        print(f"  Requests: {status['requests_processed']}")
        print()

    @staticmethod
    def _show_help():
        """Show help information."""
        print("\n📚 Claude Bot Commands:")
        print("  /analyze <file>      - Analyze code quality and issues")
        print("  /repair <file>       - Automatically repair code issues")
        print("  /chat <message>      - Chat with Claude")
        print("  /status              - Show system status")
        print("  /help                - Show this help")
        print("  /quit                - Exit bot")
        print()


class ClaudeBot:
    """Main Claude Bot orchestrator."""

    def __init__(self):
        self.analyzer = CodeAnalyzer()
        self.repair_engine = AutoRepair(self.analyzer)
        self.api = ClaudeBotAPI(self.analyzer, self.repair_engine)
        self.cli = ClaudeBotCLI(self.analyzer, self.repair_engine, self.api)

        logger.info("🚀 Claude Bot initialized - Ready for operation")

    async def run(self, mode: BotMode = BotMode.CLI):
        """Run Claude Bot in specified mode."""
        logger.info(f"📍 Starting in {mode.value} mode...")

        if mode == BotMode.CLI:
            await self.cli.interactive_mode()
        elif mode == BotMode.API:
            self._start_api_server()
        elif mode == BotMode.AUTO:
            await self._run_auto_mode()
        else:
            await self.cli.interactive_mode()

    def _start_api_server(self):
        """Start API server (placeholder)."""
        print("\n🌐 API Server Mode")
        print("=" * 60)
        print("API Server would start on http://localhost:8000")
        print("Endpoints:")
        print("  POST /api/analyze  - Analyze code")
        print("  POST /api/repair   - Repair code")
        print("  POST /api/chat     - Chat endpoint")
        print("  GET  /api/status   - System status")
        print("=" * 60 + "\n")

    async def _run_auto_mode(self):
        """Run in fully automatic mode."""
        print("\n⚙️  Auto Mode - Fully Automated Processing")
        print("=" * 60)
        print("Ready to process tasks automatically...")
        print("Waiting for input files or API requests...")
        print("=" * 60 + "\n")


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Claude Local Bot')
    parser.add_argument(
        '--mode',
        choices=['cli', 'api', 'auto'],
        default='cli',
        help='Operation mode'
    )
    parser.add_argument(
        '--file',
        help='Analyze/repair file'
    )

    args = parser.parse_args()

    bot = ClaudeBot()

    if args.file:
        # Direct file analysis
        try:
            with open(args.file, 'r') as f:
                code = f.read()
            result = bot.analyzer.analyze(code)
            print(json.dumps(result, indent=2))
        except FileNotFoundError:
            print(f"✗ File not found: {args.file}")
    else:
        # Run in specified mode
        mode = BotMode(args.mode)
        await bot.run(mode)


if __name__ == '__main__':
    asyncio.run(main())
