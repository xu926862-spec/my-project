# Claude API Chatbot 🤖

A simple, independent chatbot powered by the Claude API. No dependencies beyond the Anthropic Python SDK.

## Features

- ✅ Interactive multi-turn conversations
- ✅ Persistent conversation history
- ✅ Customizable system prompts
- ✅ Switch between Claude models
- ✅ Clear and simple API
- ✅ Error handling and retry logic built-in

## Setup

### 1. Install Dependencies

```bash
pip install anthropic
```

### 2. Set Your API Key

You need your own Anthropic API key. Get one from [console.anthropic.com](https://console.anthropic.com).

**Option A: Environment Variable (Recommended)**
```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

**Option B: Set in Shell (Temporary)**
```bash
ANTHROPIC_API_KEY='sk-ant-...' python claude_chatbot.py
```

## Usage

### Interactive Chat

```bash
python claude_chatbot.py
```

This starts an interactive chat session where you can:
- Type messages to chat with Claude
- Use commands to control the bot

### Commands

- `/clear` - Clear conversation history
- `/reset` - Reset to default system prompt
- `/system <prompt>` - Set a custom system prompt
- `/model <name>` - Change the Claude model (e.g., `claude-opus-5`, `claude-sonnet-5`)
- `/quit` - Exit the chatbot

### Single Query Demo

```bash
python claude_chatbot.py --demo
```

Runs a single query and exits.

## Example Usage

```
🤖 Claude Chatbot
==================================================
Commands:
  /clear  - Clear conversation history
  /reset  - Reset system prompt to default
  /system - Set custom system prompt
  /model  - Change model
  /quit   - Exit the chatbot
==================================================

✓ Connected to Claude API (Model: claude-opus-5)
✓ System prompt: You are a helpful, friendly AI assistant...

You: What's the capital of France?
Claude: The capital of France is Paris. It's located in the north-central part of the country on the Seine River. Paris is known as the "City of Light" and is famous for landmarks like the Eiffel Tower, Notre-Dame Cathedral, and the Louvre Museum.

You: /system You are a Python expert assistant.
✓ System prompt updated: You are a Python expert assistant.

You: How do I read a JSON file?
Claude: Here's how to read a JSON file in Python...

You: /quit
👋 Goodbye!
```

## Python API

You can also use the chatbot programmatically:

```python
from claude_chatbot import ClaudeChatbot

# Create a chatbot instance
bot = ClaudeChatbot(
    model="claude-opus-5",
    system_prompt="You are a helpful assistant.",
    temperature=0.7
)

# Send a message
response = bot.chat("Hello! How are you?")
print(response)

# Continue the conversation
response2 = bot.chat("Tell me more about that.")
print(response2)

# Clear history
bot.clear_history()
```

## Available Models

- `claude-opus-5` (default) - Most capable, best for complex tasks
- `claude-sonnet-5` - Balanced performance and cost
- `claude-haiku-4-5` - Fast and efficient for simple tasks
- `claude-fable-5-1` - Latest frontier model

See [Anthropic's documentation](https://docs.anthropic.com/claude/latest/using-the-api/models-overview) for the latest model list.

## Error Handling

The chatbot automatically:
- Retries on rate limits and server errors
- Validates API credentials
- Provides clear error messages

## Cost

Pricing depends on the model:
- **Claude Opus 5**: $5/MTok input, $25/MTok output
- **Claude Sonnet 5**: $2/MTok input, $10/MTok output
- **Claude Haiku 4.5**: $1/MTok input, $5/MTok output

Use `--demo` to test with a single query, or check token usage in the Anthropic console.

## Architecture

```
claude_chatbot.py
├── ClaudeChatbot class
│   ├── __init__() - Setup with API key
│   ├── chat() - Send message and get response
│   ├── clear_history() - Reset conversation
│   └── system_prompt/model - Configurable parameters
└── Main functions
    ├── interactive_chat() - REPL mode
    ├── demo_single_query() - Demo mode
    └── main() - Entry point
```

## Troubleshooting

### "ANTHROPIC_API_KEY environment variable not set"
Set your API key:
```bash
export ANTHROPIC_API_KEY='your-key-here'
python claude_chatbot.py
```

### "APIError: Unauthorized"
Your API key is invalid or expired. Get a new one from console.anthropic.com.

### "APIError: Rate Limit Exceeded"
The SDK automatically retries. If you hit hard limits, wait a bit and try again.

### "APIError: Model not found"
Check the model name. Available models: `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5`, etc.

## License

Open source - use as you like!
