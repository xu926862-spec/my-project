#!/bin/bash
# Claude Local Bot Launcher
# Hybrid system: CLI + API + Code Analysis + Auto-Repair
# Powered by Claude 3.5

set -e

echo "🤖 Claude Local Bot v3.5"
echo "========================================"
echo "All-in-One AI Assistant"
echo "Code Analysis | Auto-Repair | Chat | API"
echo "========================================"
echo ""

# Check if bot script exists
if [ ! -f "claude_bot.py" ]; then
    echo "✗ claude_bot.py not found"
    exit 1
fi

# Display available modes
echo "📋 Available Modes:"
echo "  --mode cli       Interactive CLI mode (default)"
echo "  --mode api       REST API server"
echo "  --mode auto      Fully automated processing"
echo ""

# Display capabilities
echo "✨ Capabilities:"
echo "  ✓ Code Analysis (7+ languages)"
echo "  ✓ Automatic Code Repair"
echo "  ✓ AI Chat Interface"
echo "  ✓ REST API Server"
echo "  ✓ Performance Analysis"
echo "  ✓ Security Review"
echo ""

# Parse arguments
MODE="cli"
FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --file)
            FILE="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Run bot
echo "▶️  Starting Claude Bot..."
echo ""

if [ -z "$FILE" ]; then
    python claude_bot.py --mode "$MODE"
else
    python claude_bot.py --mode "$MODE" --file "$FILE"
fi
