#!/usr/bin/env python3
"""
Example usage of the Claude Chatbot API.
Shows how to use the chatbot programmatically.
"""

import os
from claude_chatbot import ClaudeChatbot


def example_basic_usage():
    """Basic usage example."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)

    try:
        chatbot = ClaudeChatbot()
        response = chatbot.chat("What is 2 + 2?")
        print(f"Q: What is 2 + 2?")
        print(f"A: {response}\n")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable\n")


def example_conversation():
    """Multi-turn conversation example."""
    print("=" * 60)
    print("Example 2: Multi-turn Conversation")
    print("=" * 60)

    try:
        chatbot = ClaudeChatbot()

        # First turn
        q1 = "What's an interesting fact about Python?"
        print(f"Q1: {q1}")
        r1 = chatbot.chat(q1)
        print(f"A1: {r1[:100]}...\n")

        # Follow-up turn (history is preserved)
        q2 = "How is that different from JavaScript?"
        print(f"Q2: {q2}")
        r2 = chatbot.chat(q2)
        print(f"A2: {r2[:100]}...\n")

    except ValueError as e:
        print(f"Error: {e}\n")


def example_custom_system_prompt():
    """Using a custom system prompt."""
    print("=" * 60)
    print("Example 3: Custom System Prompt")
    print("=" * 60)

    try:
        chatbot = ClaudeChatbot(
            system_prompt="You are a brief, professional technical writer. Keep responses concise."
        )

        q = "Explain machine learning in one sentence."
        print(f"Q: {q}")
        response = chatbot.chat(q)
        print(f"A: {response}\n")

    except ValueError as e:
        print(f"Error: {e}\n")


def example_different_models():
    """Using different models."""
    print("=" * 60)
    print("Example 4: Different Models")
    print("=" * 60)

    models = [
        ("claude-haiku-4-5", "Fast"),
        ("claude-sonnet-5", "Balanced"),
        ("claude-opus-5", "Most Capable"),
    ]

    question = "What is AI?"

    for model, description in models:
        try:
            chatbot = ClaudeChatbot(model=model)
            print(f"\nModel: {model} ({description})")
            print("-" * 40)
            response = chatbot.chat(question)
            print(f"Response: {response[:150]}...")
        except ValueError as e:
            print(f"Error: {e}")
            break


def example_conversation_history():
    """Accessing conversation history."""
    print("=" * 60)
    print("Example 5: Conversation History")
    print("=" * 60)

    try:
        chatbot = ClaudeChatbot()

        # Add some messages
        chatbot.chat("My name is Alice")
        chatbot.chat("What's my name?")
        chatbot.chat("Tell me a joke")

        print(f"Conversation history ({chatbot.get_history_length()} messages):")
        print("-" * 40)

        for i, msg in enumerate(chatbot.conversation_history, 1):
            role = msg["role"].upper()
            content = msg["content"][:60]
            print(f"{i}. {role}: {content}...")

        print()

    except ValueError as e:
        print(f"Error: {e}\n")


def main():
    """Run all examples."""
    print("\n🤖 Claude Chatbot - Usage Examples\n")

    # Check if API key is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set!")
        print("Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
        print("\nRunning examples with error handling...\n")

    example_basic_usage()
    example_conversation()
    example_custom_system_prompt()
    example_different_models()
    example_conversation_history()

    print("=" * 60)
    print("Examples complete! Use claude_chatbot.py for interactive chat.")
    print("=" * 60)


if __name__ == "__main__":
    main()
