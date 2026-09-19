import os
import json
from datetime import datetime
from claude_client import ClaudeClient

class ChatbotApp:
    """完整的本地聊天机器人应用"""
    
    def __init__(self, model="llama2", history_file="chat_history.json"):
        self.client = ClaudeClient(model=model, use_local=True)
        self.history_file = history_file
        self.load_history()
    
    def load_history(self):
        """加载会话历史"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.client.conversation_history = json.load(f)
    
    def save_history(self):
        """保存会话历史"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.client.conversation_history, f, ensure_ascii=False, indent=2)
    
    def run(self):
        """启动交互式聊天"""
        print("\n" + "="*50)
        print("🤖 本地 AI 聊天机器人")
        print("="*50)
        print("命令:")
        print("  /quit     - 退出")
        print("  /clear    - 清空历史")
        print("  /save     - 保存历史")
        print("  /history  - 显示历史")
        print("="*50 + "\n")
        
        while True:
            try:
                user_input = input("你: ").strip()
                
                if not user_input:
                    continue
                
                if user_input == "/quit":
                    self.save_history()
                    print("\n再见! 💙")
                    break
                
                elif user_input == "/clear":
                    self.client.clear_history()
                    print("✅ 历史已清空\n")
                
                elif user_input == "/save":
                    self.save_history()
                    print("✅ 历史已保存\n")
                
                elif user_input == "/history":
                    print("\n📝 对话历史:")
                    for msg in self.client.conversation_history:
                        role = "你" if msg["role"] == "user" else "机器人"
                        print(f"{role}: {msg['content']}\n")
                
                else:
                    print("\n机器人: ", end="", flush=True)
                    response = self.client.send(user_input)
                    print(response + "\n")
                    self.save_history()
            
            except KeyboardInterrupt:
                self.save_history()
                print("\n\n再见! 💙")
                break
            except Exception as e:
                print(f"❌ 错误: {e}\n")

if __name__ == "__main__":
    app = ChatbotApp(model="llama2")
    app.run()
