#!/usr/bin/env python3
"""
Claude API Chatbot - An independent chatbot using the Claude API.
Requires ANTHROPIC_API_KEY environment variable.
"""

import os
import sys
from typing import Optional
from pathlib import Path
import anthropic


class ClaudeChatbot:
    """Simple chatbot powered by Claude API."""

    def __init__(
        self,
        model: str = "claude-opus-5",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
    ):
        """Initialize the chatbot with Claude API configuration."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Please set your API key: export ANTHROPIC_API_KEY='your-key-here'"
            )

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt or "You are a helpful, friendly AI assistant."
        self.conversation_history = []

    def chat(self, user_message: str) -> str:
        """Send a message and get a response from Claude."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
        })

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=self.system_prompt,
                messages=self.conversation_history,
            )

            assistant_message = ""
            for block in response.content:
                if block.type == "text":
                    assistant_message += block.text

            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message,
            })

            return assistant_message

        except anthropic.APIError as e:
            error_msg = f"API Error: {str(e)}"
            print(f"\n❌ {error_msg}", file=sys.stderr)
            raise

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []

    def get_history_length(self) -> int:
        """Get the number of messages in conversation history."""
        return len(self.conversation_history)


def interactive_chat():
    """Run the chatbot in interactive mode."""
    print("🤖 Claude Chatbot")
    print("=" * 50)
    print("Commands:")
    print("  /clear  - Clear conversation history")
    print("  /reset  - Reset system prompt to default")
    print("  /system - Set custom system prompt")
    print("  /model  - Change model")
    print("  /quit   - Exit the chatbot")
    print("=" * 50)
    print()

    system_prompt = "You are a helpful, friendly AI assistant."
    model = "claude-opus-5"

    try:
        chatbot = ClaudeChatbot(model=model, system_prompt=system_prompt)
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ Connected to Claude API (Model: {model})")
    print(f"✓ System prompt: {system_prompt[:50]}...")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "/quit":
                print("👋 Goodbye!")
                break

            if user_input.lower() == "/clear":
                chatbot.clear_history()
                print("✓ Conversation history cleared")
                continue

            if user_input.lower() == "/reset":
                chatbot.system_prompt = "You are a helpful, friendly AI assistant."
                chatbot.clear_history()
                print("✓ System prompt reset and history cleared")
                continue

            if user_input.lower().startswith("/system "):
                new_prompt = user_input[8:].strip()
                if new_prompt:
                    chatbot.system_prompt = new_prompt
                    chatbot.clear_history()
                    print(f"✓ System prompt updated: {new_prompt[:50]}...")
                continue

            if user_input.lower().startswith("/model "):
                new_model = user_input[7:].strip()
                if new_model:
                    chatbot.model = new_model
                    chatbot.clear_history()
                    print(f"✓ Model changed to: {new_model}")
                continue

            print("Claude: ", end="", flush=True)
            response = chatbot.chat(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except anthropic.APIError as e:
            print(f"❌ API Error: {e}", file=sys.stderr)
            continue


def demo_single_query():
    """Run a single query demo."""
    try:
        chatbot = ClaudeChatbot()
        print("🤖 Claude Chatbot - Single Query Demo")
        print("=" * 50)
        print()

        query = "What's an interesting fact about machine learning?"
        print(f"You: {query}")
        print()

        print("Claude: ", end="", flush=True)
        response = chatbot.chat(query)
        print(response)
        print()

    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_single_query()
    else:
        interactive_chat()


if __name__ == "__main__":
    main()
