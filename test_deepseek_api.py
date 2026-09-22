#!/usr/bin/env python3
"""
DeepSeek API 连接测试脚本
用于验证 API 密钥和连接

使用方法:
    export DEEPSEEK_API_KEY='your-api-key'
    python3 test_deepseek_api.py
"""

import os
import json
import urllib.request
from typing import Optional

# 配置
API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"
DEFAULT_MODEL = "deepseek-chat"

# 颜色
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_header(text: str):
    """打印标题"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def check_api_key() -> bool:
    """检查 API 密钥"""
    print("🔑 检查 API 密钥...")

    if not API_KEY:
        print(f"{RED}✗ 未找到 DEEPSEEK_API_KEY 环境变量{RESET}")
        print(f"{YELLOW}请设置: export DEEPSEEK_API_KEY='your-key'{RESET}")
        return False

    if len(API_KEY) < 20:
        print(f"{RED}✗ API 密钥长度过短{RESET}")
        return False

    print(f"{GREEN}✓ API 密钥已设置{RESET}")
    print(f"   长度: {len(API_KEY)} 字符")
    return True


def test_basic_connection() -> bool:
    """测试基本连接"""
    print("\n📡 测试基本连接...")

    try:
        # 测试 DNS 解析
        import socket
        socket.gethostbyname("api.deepseek.com")
        print(f"{GREEN}✓ DNS 解析正常{RESET}")

        # 测试 API 端点连接
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }

        payload = {
            "model": DEFAULT_MODEL,
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "temperature": 0.5,
            "max_tokens": 10,
            "stream": False
        }

        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        print(f"{BLUE}发送测试请求到 {API_URL}...{RESET}")

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                response_data = json.loads(response.read().decode('utf-8'))

                if 'choices' in response_data:
                    print(f"{GREEN}✓ API 连接成功{RESET}")
                    print(f"  模型: {response_data.get('model')}")
                    print(f"  状态码: {response.status}")

                    if 'usage' in response_data:
                        usage = response_data['usage']
                        print(f"  使用: input={usage.get('prompt_tokens')}, "
                              f"output={usage.get('completion_tokens')}")

                    return True
                else:
                    print(f"{RED}✗ 无效的 API 响应{RESET}")
                    print(json.dumps(response_data, indent=2, ensure_ascii=False))
                    return False

        except urllib.error.HTTPError as e:
            error_msg = e.read().decode('utf-8')
            print(f"{RED}✗ API 错误 ({e.code}): {e.reason}{RESET}")
            print(f"  {error_msg}")

            if e.code == 401:
                print(f"{YELLOW}  提示: API 密钥可能无效或已过期{RESET}")
            elif e.code == 429:
                print(f"{YELLOW}  提示: 请求过于频繁，请稍后再试{RESET}")

            return False

    except Exception as e:
        print(f"{RED}✗ 连接失败: {e}{RESET}")
        return False


def test_models() -> bool:
    """测试各个模型"""
    print("\n🤖 测试可用模型...")

    models = {
        "chat": "deepseek-chat",
        "reasoner": "deepseek-reasoner-1215",
        "coder": "deepseek-coder-67b"
    }

    for alias, model_name in models.items():
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }

            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": "Hi"}],
                "temperature": 0.5,
                "max_tokens": 5
            }

            req = urllib.request.Request(
                API_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                response.read()
                print(f"{GREEN}✓ {alias:10} ({model_name}){RESET}")

        except Exception as e:
            print(f"{RED}✗ {alias:10} ({model_name}){RESET}")
            print(f"  错误: {str(e)[:50]}")


def get_account_info() -> bool:
    """获取账户信息（如果可用）"""
    print("\n💰 获取账户信息...")

    try:
        # 注: DeepSeek API 可能不提供此端点
        print(f"{YELLOW}⊘ 账户信息端点暂不可用{RESET}")
        return True
    except:
        return False


def main():
    """主函数"""
    print_header("DeepSeek API 连接测试")

    print(f"测试环境: Python 3")
    print(f"API 端点: {API_URL}")
    print(f"默认模型: {DEFAULT_MODEL}\n")

    # 测试序列
    tests = [
        ("API 密钥检查", check_api_key),
        ("基本连接", test_basic_connection),
        ("模型测试", test_models),
        ("账户信息", get_account_info),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"{RED}✗ {test_name} 出错: {e}{RESET}")
            results.append((test_name, False))

    # 总结
    print_header("测试总结")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = f"{GREEN}✓ PASS{RESET}" if result else f"{RED}✗ FAIL{RESET}"
        print(f"{status} - {test_name}")

    print(f"\n结果: {passed}/{total} 测试通过")

    if passed == total:
        print(f"\n{GREEN}🎉 所有测试通过！{RESET}")
        print(f"\n✅ 您可以开始使用 DeepSeek API:")
        print(f"   cd claude_bot_v3.5")
        print(f"   python3 claude_bot.py chat 'Hello'")
    else:
        print(f"\n{RED}❌ 有些测试失败{RESET}")
        print(f"{YELLOW}请检查上面的错误信息并重试{RESET}")

    return passed == total


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
