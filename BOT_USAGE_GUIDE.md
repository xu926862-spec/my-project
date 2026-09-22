# Claude Bot v3.5 with DeepSeek Integration - Complete Usage Guide

## Quick Start

### 1. Set Your DeepSeek API Key
```bash
export DEEPSEEK_API_KEY='sk-your-api-key-here'
```

### 2. Run the Bot

#### **Chat Mode** - Ask Questions
```bash
# Single question
python3 deepseek_bot.py chat "用 Python 写一个单例模式"

# Interactive chat
python3 deepseek_bot.py chat
```

#### **Scan Mode** - Analyze Your Project
```bash
# Scan current directory
python3 deepseek_bot.py scan

# Scan specific directory
python3 deepseek_bot.py scan --dir ./src

# Save report to JSON
python3 deepseek_bot.py scan --output report.json
```

#### **Repair Mode** - Auto-Fix Code
```bash
# Auto-fix a Python file
python3 deepseek_bot.py repair --target data/sample.py

# This will:
# 1. Analyze the code for bugs and issues
# 2. Send it to DeepSeek for optimization
# 3. Automatically create a .bak backup
# 4. Write the fixed code back to the file
```

---

## Available Versions

### 1. **deepseek_bot.py** (Pure Edition)
- Lightweight, zero external dependencies
- Commands: `chat`, `scan`, `repair`
- Perfect for: Quick text input processing
- Size: ~250 lines

### 2. **claude_bot_v3.5/claude_bot.py** (Standard Edition)
- Feature-complete version
- Commands: `chat`, `analyze`, `models`
- Perfect for: General-purpose AI assistant
- Size: ~247 lines

### 3. **claude_bot_v3.5/claude_bot_advanced.py** (Advanced Edition)
- Enterprise-grade features
- Multi-model support (chat, reasoner, coder)
- Enhanced error handling and statistics
- Size: ~273 lines

### 4. **interactive_deepseek.py** (Interactive Processor)
- Rich terminal UI
- Session management
- Model switching on-the-fly
- Conversation history tracking
- Commands: `/help`, `/model`, `/clear`, `/stats`, `/exit`

---

## Example Workflow

### Example 1: Understand Python Singleton Patterns
```bash
python3 deepseek_bot.py chat "用 Python 写一个单例模式，并解释各个方法的优缺点"
```

### Example 2: Analyze Your Project Structure
```bash
python3 deepseek_bot.py scan --dir . --output project_stats.json
```

### Example 3: Auto-Fix Code Issues
```bash
# Let DeepSeek analyze and fix your code
python3 deepseek_bot.py repair --target your_file.py

# The bot will:
# - Read the file
# - Send to AI for analysis
# - Fix issues (bugs, security, performance)
# - Create automatic backup (your_file.py.bak)
# - Write optimized code back
```

### Example 4: Interactive Session
```bash
python3 interactive_deepseek.py

# Then:
# Input: 请解释装饰器模式
# Output: [AI response with explanation]
# 
# Input: /model
# Select: 2 (deepseek-reasoner-1215 for complex reasoning)
#
# Input: 如何在生产环境中使用这个模式？
# Output: [Response using reasoning model]
#
# Input: /stats
# Shows: conversation stats, token usage
#
# Input: /exit
# Exit session
```

---

## Available Models

### 1. **deepseek-chat** (Default)
- Standard conversational model
- Best for: General questions, explanations
- Speed: Fast
- Use case: Default choice for most queries

### 2. **deepseek-reasoner-1215** (DeepSeek 3.5)
- Advanced reasoning model
- Best for: Complex problems, analysis
- Speed: Slower (more thorough)
- Use case: When you need deep thinking

### 3. **deepseek-coder-67b**
- Specialized code model
- Best for: Code generation, debugging
- Speed: Medium
- Use case: Programming tasks

---

## Features Included

### ✅ Core Features
- [x] Chat with DeepSeek API
- [x] Workspace project scanning
- [x] Automatic code repair with AI
- [x] Safe file write-back with backups
- [x] Multi-model support
- [x] Terminal color formatting
- [x] JSON report export
- [x] Conversation history tracking

### ✅ Safety Features
- [x] Automatic .bak backup creation before file modifications
- [x] UTF-8 encoding with error handling
- [x] Timeout protection (30 seconds)
- [x] Comprehensive error messages
- [x] API key validation

### ✅ Advanced Features
- [x] Interactive mode with command support
- [x] Project statistics and analysis
- [x] Token usage tracking
- [x] Model switching capability
- [x] Conversation context persistence

---

## Environment Configuration

Create `.env` file (optional):
```bash
export DEEPSEEK_API_KEY='sk-xxxxx'
export API_BASE_URL='https://api.deepseek.com/v1/chat/completions'
export DEFAULT_MODEL='deepseek-chat'
export API_TIMEOUT='30'
```

Or set directly:
```bash
export DEEPSEEK_API_KEY='your-key'
python3 deepseek_bot.py chat "Your question here"
```

---

## Real-World Examples

### 1. Code Review
```bash
python3 deepseek_bot.py repair --target buggy_module.py
```

### 2. Project Analysis
```bash
python3 deepseek_bot.py scan --output stats.json
cat stats.json  # View detailed statistics
```

### 3. Learning Programming Concepts
```bash
python3 deepseek_bot.py chat "解释设计模式中的工厂模式，并给出 Python 实现"
```

### 4. Debugging Help
```bash
python3 deepseek_bot.py chat "为什么这段代码会产生 TypeError？<paste code here>"
```

---

## Troubleshooting

### Issue: "Error: 未检测到 DEEPSEEK_API_KEY"
**Solution:** Set the environment variable:
```bash
export DEEPSEEK_API_KEY='sk-your-api-key'
```

### Issue: "API Error: Connection timeout"
**Solution:** Check internet connection, verify API key is valid

### Issue: "File not found"
**Solution:** Provide absolute path or check file exists:
```bash
python3 deepseek_bot.py repair --target /absolute/path/to/file.py
```

### Issue: "Invalid choice: 'scan'"
**Solution:** Make sure you're using `deepseek_bot.py`, not `claude_bot_v3.5/claude_bot.py`
```bash
python3 deepseek_bot.py scan  # ✅ Correct
python3 claude_bot_v3.5/claude_bot.py scan  # ❌ Wrong (different commands)
```

---

## Python Singleton Pattern Reference

For your specific question about Python singleton patterns, see: `examples/singleton_pattern.py`

This file includes:
1. **Decorator-based** (Recommended - simplest)
2. **Metaclass-based** (Most pythonic)
3. **__new__ method** (Most flexible)
4. **Module-level** (Simplest for single instance)
5. **Thread-safe** (For multi-threaded environments)

Plus performance benchmarks comparing all 5 approaches!

---

## API Response Format

The bot returns AI responses in this format:

```
✓ DeepSeek Bot v3.5 已初始化
  模型: deepseek-chat

[Request #1] 调用 DeepSeek 3.5 (deepseek-chat)...
[Stats] Input: 45, Output: 382

--- DeepSeek 回复 ---
<AI response here>
------------------
```

---

## Next Steps

1. **Set your API key**: `export DEEPSEEK_API_KEY='sk-...'`
2. **Try a simple query**: `python3 deepseek_bot.py chat "Hello"`
3. **Scan your project**: `python3 deepseek_bot.py scan`
4. **Fix a file**: `python3 deepseek_bot.py repair --target your_file.py`
5. **Go interactive**: `python3 interactive_deepseek.py`

---

## System Requirements

- Python 3.6+
- Internet connection (for API calls)
- Valid DeepSeek API key
- No external dependencies (uses only urllib, json, os, sys)

---

Generated with Claude Code
