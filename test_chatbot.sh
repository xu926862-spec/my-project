#!/bin/bash
echo "🤖 Testing Claude Chatbot..."
echo "======================================"

# Check if anthropic package is installed
python3 -c "import anthropic; print('✓ anthropic package installed')" 2>/dev/null || {
    echo "⚠️  anthropic not installed. Installing..."
    pip install anthropic -q
}

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set"
    echo "To test the chatbot, set: export ANTHROPIC_API_KEY='sk-ant-...'"
    echo ""
    echo "Running syntax and import check instead..."
    python3 -c "
from claude_chatbot import ClaudeChatbot
print('✓ Chatbot module imports successfully')
print('✓ ClaudeChatbot class is available')
print('✓ Ready to use when API key is provided')
"
else
    echo "✓ API key is set"
    echo ""
    echo "Testing single query..."
    python3 claude_chatbot.py --demo
fi
