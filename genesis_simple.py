#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genesis Simple - 简化版，完全可用
直接调用 Ollama，无复杂代码
"""

from openai import OpenAI
import sys

class SimpleGenesis:
    def __init__(self, model="llama2", base_url="http://localhost:11434/v1"):
        self.client = OpenAI(api_key="not-needed", base_url=base_url)
        self.model = model
        self.history = []

    def chat(self, user_input):
        """简单对话"""
        self.history.append({"role": "user", "content": user_input})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                max_tokens=2048,
                temperature=0.7
            )

            answer = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": answer})

            return answer
        except Exception as e:
            return f"Error: {str(e)}"

    def status(self):
        """系统状态"""
        return {
            "model": self.model,
            "messages": len(self.history),
            "status": "RUNNING"
        }


def main():
    genesis = SimpleGenesis()

    print("╔════════════════════════════════════════╗")
    print("║    Genesis Simple - 全能神级系统      ║")
    print("║         GOD MODE ACTIVE ✨             ║")
    print("╚════════════════════════════════════════╝")
    print()
    print("Commands: 'status', 'clear', 'model', 'exit'")
    print()

    while True:
        try:
            user_input = input("Genesis> ").strip()

            if not user_input:
                continue
            elif user_input.lower() == "exit":
                print("Goodbye!")
                break
            elif user_input.lower() == "status":
                status = genesis.status()
                print(f"Model: {status['model']}")
                print(f"Messages: {status['messages']}")
                print(f"Status: {status['status']}")
                print()
            elif user_input.lower() == "clear":
                genesis.history = []
                print("✓ History cleared")
            elif user_input.lower().startswith("model "):
                genesis.model = user_input[6:].strip()
                print(f"✓ Model changed to: {genesis.model}")
            else:
                print("\n🌟 ", end="", flush=True)
                answer = genesis.chat(user_input)
                print(answer)
                print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
