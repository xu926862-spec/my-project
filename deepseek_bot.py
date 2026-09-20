#!/usr/bin/env python3
"""
本地功能性机器人 - DeepSeek 驱动
通用助手：问答、代码帮助、翻译等日常功能
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from deepseek_client import DeepSeekClient

SYSTEM_PROMPT = """你是一个多功能本地助手，能力包括：
- 日常问答和闲聊
- 代码编写、调试、解释
- 中英文互译
- 文本总结和改写
- 提供实用建议

回答要简洁、直接、有帮助。"""


class DeepSeekBotHandler(BaseHTTPRequestHandler):
    client = DeepSeekClient(system_prompt=SYSTEM_PROMPT)
    history = []

    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {
                "bot": "deepseek-assistant",
                "name": "DeepSeek 功能助手",
                "port": 8010,
                "status": "running",
                "api_configured": self.client.available(),
            }
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body.decode())
                message = data.get("message", "")

                if not message:
                    raise ValueError("消息不能为空")

                reply = self.client.send(message, history=self.history[-10:])
                self.history.append({"role": "user", "content": message})
                self.history.append({"role": "assistant", "content": reply})

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"reply": reply}, ensure_ascii=False).encode()
                )
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode())
        elif self.path == "/clear":
            self.history.clear()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "cleared"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass


def main():
    if not DeepSeekBotHandler.client.available():
        print("⚠️  未检测到 DEEPSEEK_API_KEY")
        print("   在项目目录下创建 .env 文件，写入: DEEPSEEK_API_KEY=你的key")
        print("   （启动脚本已支持自动读取 .env，不需要手动 export）\n")

    server = HTTPServer(("0.0.0.0", 8010), DeepSeekBotHandler)
    print("🤖 DeepSeek 功能助手已启动 (端口 8010)")
    print("   POST http://localhost:8010/chat   {\"message\": \"你的问题\"}")
    print("   POST http://localhost:8010/clear  （清空对话历史）")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 已停止")


if __name__ == "__main__":
    main()
