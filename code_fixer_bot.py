#!/usr/bin/env python3
"""
代码修复助手 - HTTP 服务版
用途：粘贴代码，分析、修复、优化建议
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from deepseek_client import DeepSeekClient

SYSTEM_PROMPT = """你是一个专业的代码审查和优化专家。能力包括：
- 分析和修复所有编程语言的代码
- 识别 bug 和性能问题
- 优化算法和代码结构
- 提供最佳实践建议
- 解释代码的工作原理

对每个问题都提供：
1. 问题分析（具体问题在哪）
2. 修复方案（如何解决）
3. 改进代码（修复后的代码）
4. 最佳实践（如何避免）"""


class CodeFixerHandler(BaseHTTPRequestHandler):
    client = DeepSeekClient(system_prompt=SYSTEM_PROMPT)
    history = []

    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {
                "bot": "code-fixer",
                "name": "代码修复助手",
                "port": 8002,
                "status": "running",
                "api_configured": self.client.available(),
            }
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/fix":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode())
                code = data.get("code", "")

                if not code:
                    raise ValueError("code 不能为空")

                reply = self.client.send(code, history=self.history[-6:])
                self.history.append({"role": "user", "content": code})
                self.history.append({"role": "assistant", "content": reply})

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"reply": reply}, ensure_ascii=False).encode())
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
    server = HTTPServer(("0.0.0.0", 8002), CodeFixerHandler)
    print("🔧 代码修复助手已启动 (端口 8002)")
    print("   POST http://localhost:8002/fix   {\"code\": \"你的代码\"}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 已停止")


if __name__ == "__main__":
    main()
