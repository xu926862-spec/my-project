#!/usr/bin/env python3
"""
交互式 DeepSeek API 文本输入处理系统
接收用户输入，通过 DeepSeek API 处理并返回结果

使用方法:
    export DEEPSEEK_API_KEY='your-api-key'
    python3 interactive_deepseek.py
"""

import os
import sys
import json
import urllib.request
from typing import Optional, Dict, Any

# 配置
API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

# 颜色输出
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# 模型列表
MODELS = {
    "1": ("deepseek-chat", "标准聊天模型"),
    "2": ("deepseek-reasoner-1215", "推理模型 (DeepSeek 3.5)"),
    "3": ("deepseek-coder-67b", "代码专家模型"),
}


class DeepSeekTextProcessor:
    """DeepSeek API 文本处理器"""

    def __init__(self, model: str = "deepseek-chat"):
        self.api_key = API_KEY
        self.model = model
        self.conversation_history = []
        self.total_tokens = 0

        if not self.api_key:
            print(f"{RED}❌ 错误: 未设置 DEEPSEEK_API_KEY 环境变量{RESET}")
            sys.exit(1)

    def process_text(self, user_input: str, temperature: float = 0.5) -> Optional[Dict[str, Any]]:
        """处理用户输入文本"""

        # 添加到对话历史
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        try:
            # 构建请求
            payload = {
                "model": self.model,
                "messages": self.conversation_history,
                "temperature": temperature,
                "stream": False,
                "top_p": 0.95,
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            # 发送请求
            req = urllib.request.Request(
                API_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )

            print(f"{CYAN}⏳ 正在处理...{RESET}")

            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = json.loads(response.read().decode('utf-8'))

                if 'choices' in response_data:
                    # 提取回复
                    assistant_message = response_data['choices'][0]['message']['content']

                    # 添加到对话历史
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": assistant_message
                    })

                    # 统计 tokens
                    if 'usage' in response_data:
                        usage = response_data['usage']
                        self.total_tokens += usage.get('total_tokens', 0)

                    return {
                        "success": True,
                        "content": assistant_message,
                        "model": response_data.get('model'),
                        "usage": response_data.get('usage', {}),
                    }
                else:
                    return {
                        "success": False,
                        "error": "无效的 API 响应",
                        "content": None
                    }

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            return {
                "success": False,
                "error": f"HTTP {e.code}: {e.reason}",
                "details": error_body,
                "content": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": None
            }

    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []
        print(f"{GREEN}✓ 对话历史已清除{RESET}")

    def set_model(self, model: str):
        """切换模型"""
        self.model = model
        print(f"{GREEN}✓ 已切换到模型: {model}{RESET}")

    def show_stats(self):
        """显示统计信息"""
        print(f"\n{BLUE}{'=' * 50}{RESET}")
        print(f"📊 统计信息")
        print(f"{BLUE}{'=' * 50}{RESET}")
        print(f"当前模型: {self.model}")
        print(f"对话轮数: {len(self.conversation_history) // 2}")
        print(f"总 Tokens: {self.total_tokens}")
        print(f"{BLUE}{'=' * 50}{RESET}\n")


def print_banner():
    """打印欢迎横幅"""
    print(f"\n{CYAN}{'=' * 60}{RESET}")
    print(f"{CYAN}{'🚀 DeepSeek API 交互式文本处理系统':^60}{RESET}")
    print(f"{CYAN}{'=' * 60}{RESET}")
    print(f"{GREEN}✓ 连接成功{RESET}")
    print(f"{GREEN}✓ 已准备接收输入{RESET}\n")


def show_help():
    """显示帮助信息"""
    help_text = f"""
{BLUE}{'=' * 50}{RESET}
📚 命令列表
{BLUE}{'=' * 50}{RESET}

基本命令:
  /help          - 显示此帮助信息
  /model         - 选择模型
  /clear         - 清除对话历史
  /stats         - 显示统计信息
  /exit, /quit   - 退出程序

示例:
  输入: 你好，请介绍一下自己
  输入: /model
       选择模型: 1 (聊天), 2 (推理), 3 (代码)
  输入: /clear
       清除所有对话记录

{BLUE}{'=' * 50}{RESET}
"""
    print(help_text)


def select_model() -> str:
    """选择模型"""
    print(f"\n{BLUE}{'=' * 50}{RESET}")
    print("选择模型:")
    for key, (model_name, description) in MODELS.items():
        print(f"  {key}. {description}")
    print(f"{BLUE}{'=' * 50}{RESET}")

    choice = input(f"\n{CYAN}请选择 (1-3) [{list(MODELS.keys())[0]}]: {RESET}").strip() or "1"

    if choice in MODELS:
        model_name, _ = MODELS[choice]
        return model_name
    else:
        print(f"{RED}❌ 无效选择，使用默认模型{RESET}")
        return "deepseek-chat"


def main():
    """主函数 - 交互式循环"""

    print_banner()

    # 选择初始模型
    initial_model = select_model()
    processor = DeepSeekTextProcessor(model=initial_model)

    print(f"\n{GREEN}✅ 系统已就绪！输入文本进行处理{RESET}")
    print(f"{YELLOW}💡 输入 /help 查看命令列表{RESET}\n")

    # 主循环
    message_count = 0

    while True:
        try:
            # 获取用户输入
            user_input = input(f"{CYAN}你:{RESET} ").strip()

            if not user_input:
                continue

            # 处理特殊命令
            if user_input.lower() in ['/exit', '/quit', 'exit', 'quit']:
                print(f"\n{GREEN}👋 再见！{RESET}")
                break

            elif user_input.lower() == '/help':
                show_help()
                continue

            elif user_input.lower() == '/model':
                new_model = select_model()
                processor.set_model(new_model)
                continue

            elif user_input.lower() == '/clear':
                processor.clear_history()
                continue

            elif user_input.lower() == '/stats':
                processor.show_stats()
                continue

            # 处理正常文本输入
            result = processor.process_text(user_input)

            if result["success"]:
                message_count += 1

                # 显示回复
                print(f"\n{GREEN}DeepSeek:{RESET}")
                print(f"{result['content']}\n")

                # 显示统计
                usage = result.get('usage', {})
                if usage:
                    print(f"{YELLOW}[统计] "
                          f"输入: {usage.get('prompt_tokens', 0)}, "
                          f"输出: {usage.get('completion_tokens', 0)}, "
                          f"总计: {usage.get('total_tokens', 0)}{RESET}\n")
            else:
                print(f"\n{RED}❌ 处理失败:{RESET}")
                print(f"   {result.get('error')}\n")

                if result.get('details'):
                    print(f"{YELLOW}详情: {result['details'][:100]}{RESET}\n")

        except KeyboardInterrupt:
            print(f"\n\n{GREEN}👋 已中断，再见！{RESET}")
            break
        except EOFError:
            print(f"\n{GREEN}👋 再见！{RESET}")
            break
        except Exception as e:
            print(f"{RED}❌ 错误: {e}{RESET}\n")


if __name__ == "__main__":
    main()
