#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Llama Server Agent - Zero API Cost, 100% Local LLM
Uses llama-server (llama.cpp HTTP interface) for offline inference
Compatible with OpenAI API format
"""

from openai import OpenAI
import sys

class LlamaServerAgent:
    def __init__(self, base_url: str = "http://localhost:8000/v1", model: str = "llama"):
        """
        Initialize Llama Server Agent

        Args:
            base_url: Llama server endpoint (default: localhost:8000)
            model: Model name (typically 'llama' or similar)
        """
        self.client = OpenAI(
            api_key="not-needed",  # llama-server doesn't require auth
            base_url=base_url
        )
        self.model = model

    def chat(self, messages: list, stream: bool = False, temperature: float = 0.7) -> str:
        """
        Call local llama-server

        Args:
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream response
            temperature: Model temperature (0.0-1.0)

        Returns:
            Response text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream,
                temperature=temperature,
                max_tokens=2048
            )

            if stream:
                # Collect streamed chunks
                full_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        print(content, end="", flush=True)
                print()  # newline after streaming
                return full_response
            else:
                return response.choices[0].message.content

        except Exception as e:
            return f"[ERROR] Llama server connection failed: {str(e)}\nMake sure llama-server is running at {self.client.base_url}"


def main():
    """Demo usage"""
    # Initialize agent
    agent = LlamaServerAgent()

    print("=" * 60)
    print("Llama Server Agent - Local LLM")
    print("=" * 60)

    # Example 1: Simple question
    print("\n[Test 1] Simple Question")
    print("-" * 60)
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Be concise."},
        {"role": "user", "content": "What is 2+2?"},
    ]
    response = agent.chat(messages)
    print(f"Answer: {response}\n")

    # Example 2: Code review
    print("[Test 2] Code Review")
    print("-" * 60)
    messages = [
        {"role": "system", "content": "You are an expert code reviewer. Review the code for quality, bugs, and improvements."},
        {"role": "user", "content": """
Review this Python function:

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

Point out any issues and improvements.
"""},
    ]
    response = agent.chat(messages)
    print(f"Review: {response}\n")

    # Example 3: Streaming mode
    print("[Test 3] Streaming Response")
    print("-" * 60)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain machine learning in 100 words."},
    ]
    print("Streaming: ", end="")
    response = agent.chat(messages, stream=True)
    print()

    print("\n" + "=" * 60)
    print("All tests completed!")


if __name__ == "__main__":
    main()
