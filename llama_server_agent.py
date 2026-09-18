#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude 5.1-like Local Agent - Powered by Llama Server
Features: Deep reasoning, tool calling, structured output, self-correction
Zero API Cost, 100% Local LLM Inference
"""

from openai import OpenAI
import json
from typing import Optional, Dict, List, Any, Callable

class ClaudeLikeAgent:
    def __init__(self, base_url: str = "http://localhost:8000/v1", model: str = "llama"):
        """
        Initialize Claude 5.1-like Agent powered by local llama-server

        Args:
            base_url: Llama server endpoint (default: localhost:8000)
            model: Model name
        """
        self.client = OpenAI(api_key="not-needed", base_url=base_url)
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.tools: Dict[str, Callable] = {}
        self.system_prompt = self._get_claude_system_prompt()

    def _get_claude_system_prompt(self) -> str:
        """System prompt mimicking Claude 5.1 capabilities"""
        return """You are Claude 5.1, an AI assistant with these core capabilities:

**Deep Reasoning & Analysis**
- Use step-by-step thinking for complex problems
- Break down problems into manageable components
- Consider edge cases and potential issues
- Show your reasoning process clearly

**Code Excellence**
- Generate production-quality, well-documented code
- Explain architectural decisions
- Suggest optimizations and best practices
- Handle errors and edge cases properly

**Clear Communication**
- Be precise, clear, and well-structured
- Use markdown for code, lists, and emphasis
- Explain technical concepts accessibly
- Provide actionable recommendations

**Reliability & Accuracy**
- Acknowledge uncertainty and limitations
- Suggest verification methods
- Provide multiple approaches when relevant
- Self-correct proactively

Always provide thoughtful, well-reasoned responses."""

    def register_tool(self, name: str, func: Callable, description: str = ""):
        """Register a callable tool/function"""
        self.tools[name] = {"func": func, "description": description}

    def chat(self, user_input: str, stream: bool = False) -> str:
        """
        Claude 5.1-style chat with reasoning

        Args:
            user_input: User's message
            stream: Enable streaming response

        Returns:
            Response text
        """
        self.conversation_history.append({"role": "user", "content": user_input})

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream,
                temperature=0.7,
                max_tokens=4096,
                top_p=0.95,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            if stream:
                full_response = self._handle_streaming(response)
            else:
                full_response = response.choices[0].message.content

            self.conversation_history.append({"role": "assistant", "content": full_response})
            return full_response

        except Exception as e:
            error_msg = f"[ERROR] Service unavailable: {str(e)}\nEnsure llama-server is running at {self.client.base_url}"
            return error_msg

    def _handle_streaming(self, response) -> str:
        """Collect and display streaming response"""
        full_response = ""
        for chunk in response:
            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                print(content, end="", flush=True)
        print()
        return full_response

    def analyze_code(self, code: str, language: str = "python") -> str:
        """Claude-style code analysis"""
        prompt = f"""Analyze this {language} code thoroughly:

```{language}
{code}
```

Provide:
1. **Quality Assessment**: Rate (1-10) and explain
2. **Issues**: List bugs, inefficiencies, style issues
3. **Improvements**: 3-5 specific recommendations
4. **Best Practices**: Relevant design patterns
5. **Security**: Any concerns?"""
        return self.chat(prompt)

    def debug_problem(self, problem: str, context: str = "") -> str:
        """Systematic debugging assistance"""
        prompt = f"""Debug this problem systematically:

**Problem**: {problem}
{"**Context**: " + context if context else ""}

Provide:
1. **Summary**: What's happening?
2. **Root Cause**: Why is this happening?
3. **Solutions**: Step-by-step fixes
4. **Verification**: How to confirm fix works
5. **Prevention**: How to avoid this in future"""
        return self.chat(prompt)

    def explain_concept(self, topic: str, level: str = "intermediate") -> str:
        """Deep technical explanation"""
        prompt = f"""Explain '{topic}' at {level} level:

1. **Core Idea**: Fundamental concept
2. **How It Works**: Detailed mechanism
3. **Why It Matters**: Practical importance
4. **Examples**: Real-world use cases
5. **Common Mistakes**: Pitfalls to avoid"""
        return self.chat(prompt)

    def write_documentation(self, code: str, language: str = "python") -> str:
        """Generate comprehensive documentation"""
        prompt = f"""Write documentation for this {language} code:

```{language}
{code}
```

Include:
1. **Overview**: What does this do?
2. **Parameters**: Input details
3. **Returns**: Output format
4. **Examples**: Usage examples
5. **Edge Cases**: Special considerations"""
        return self.chat(prompt)

    def code_review(self, code: str, criteria: str = "general") -> str:
        """Perform detailed code review"""
        prompt = f"""Perform {criteria} code review:

```python
{code}
```

Review for:
- Correctness and logic
- Performance optimization
- Readability and style
- Security vulnerabilities
- Testing coverage"""
        return self.chat(prompt)

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()

    def clear_history(self):
        """Reset conversation"""
        self.conversation_history = []

    def export_conversation(self, format: str = "json") -> str:
        """Export conversation"""
        if format == "json":
            return json.dumps(self.conversation_history, ensure_ascii=False, indent=2)
        elif format == "markdown":
            md = "# Conversation\n\n"
            for msg in self.conversation_history:
                role = msg["role"].upper()
                md += f"## {role}\n{msg['content']}\n\n"
            return md
        return str(self.conversation_history)


def main():
    """Interactive Claude-like agent demo"""
    agent = ClaudeLikeAgent()

    print("=" * 70)
    print("Claude 5.1-like Local Agent (Powered by Llama Server)")
    print("=" * 70)
    print()

    # Demo 1: Code Analysis
    print("[Demo 1] Code Analysis")
    print("-" * 70)
    code_sample = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    response = agent.analyze_code(code_sample)
    print(response)
    print()

    # Demo 2: Debugging Assistance
    print("[Demo 2] Debugging Assistance")
    print("-" * 70)
    response = agent.debug_problem(
        "My list comprehension returns unexpected results",
        "[x*2 for x in range(5) if x > 2]"
    )
    print(response)
    print()

    # Demo 3: Concept Explanation
    print("[Demo 3] Concept Explanation")
    print("-" * 70)
    response = agent.explain_concept("Async/Await in Python", level="beginner")
    print(response)
    print()

    # Demo 4: Interactive Chat
    print("[Demo 4] Interactive Chat")
    print("-" * 70)
    print("Type 'exit' to quit, 'history' to show conversation\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue
            elif user_input.lower() == "exit":
                print("Goodbye!")
                break
            elif user_input.lower() == "history":
                print("\n" + agent.export_conversation("markdown"))
            else:
                print("\nAgent: ", end="")
                agent.chat(user_input, stream=True)
                print()

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
