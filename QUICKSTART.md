# Claude API Chatbot - Quick Start 🚀

Get your Claude chatbot running in 5 minutes!

## Step 1: Get Your API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Create a new API key in your workspace
4. Copy your API key

## Step 2: Set Your API Key

```bash
export ANTHROPIC_API_KEY='sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

Replace with your actual API key.

## Step 3: Install Dependencies

```bash
pip install anthropic
```

Or use the provided requirements:
```bash
pip install -r chatbot_requirements.txt
```

## Step 4: Run the Chatbot

**Interactive Chat (Recommended):**
```bash
python claude_chatbot.py
```

**Single Query Demo:**
```bash
python claude_chatbot.py --demo
```

**See Examples:**
```bash
python example_chatbot_usage.py
```

## Step 5: Start Chatting!

```
🤖 Claude Chatbot
==================================================

✓ Connected to Claude API (Model: claude-opus-5)

You: Hello! How are you?
Claude: I'm doing great, thank you for asking! I'm here to help with any questions or tasks you might have. Whether you need help with writing, coding, analysis, creative projects, or just want to have a conversation, I'm ready to assist. What can I help you with today?

You: /system You are a Python expert
✓ System prompt updated: You are a Python expert

You: How do I read a JSON file in Python?
Claude: Here are a few ways to read a JSON file in Python...

You: /quit
👋 Goodbye!
```

## Available Commands

Inside the chat:

| Command | Effect |
|---------|--------|
| `/clear` | Clear conversation history |
| `/reset` | Reset to default system prompt |
| `/system <prompt>` | Set a custom system prompt |
| `/model <name>` | Switch to a different model |
| `/quit` | Exit the chatbot |

## Model Options

```bash
You: /model claude-opus-5          # Most capable (default)
You: /model claude-sonnet-5        # Balanced & faster
You: /model claude-haiku-4-5       # Fastest & cheapest
You: /model claude-fable-5-1       # Latest frontier model
```

## Python API Usage

```python
from claude_chatbot import ClaudeChatbot

# Create a chatbot
bot = ClaudeChatbot(model="claude-opus-5")

# Send a message
response = bot.chat("What's 2 + 2?")
print(response)  # "2 + 2 equals 4."

# Continue conversation (history preserved)
response2 = bot.chat("What about 3 + 3?")
print(response2)

# Custom system prompt
expert_bot = ClaudeChatbot(
    system_prompt="You are a Python expert."
)
expert_bot.chat("How do I use decorators?")
```

## Troubleshooting

**"ANTHROPIC_API_KEY environment variable not set"**
→ Run: `export ANTHROPIC_API_KEY='your-key-here'`

**"Unauthorized" error**
→ Check your API key is correct in console.anthropic.com

**"Model not found"**
→ Check available models: `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5`

**Need help?**
→ See CHATBOT_README.md for full documentation

## Files

- `claude_chatbot.py` - Main chatbot implementation
- `CHATBOT_README.md` - Full documentation
- `example_chatbot_usage.py` - Usage examples
- `chatbot_requirements.txt` - Dependencies
- `QUICKSTART.md` - This file

## Next Steps

1. ✅ Run the interactive chatbot
2. 📚 Read CHATBOT_README.md for advanced features
3. 🔧 Try example_chatbot_usage.py for different use cases
4. 💻 Integrate into your own Python code

---

**Ready?** Run `python claude_chatbot.py` now! 🎉
