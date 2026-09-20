#!/usr/bin/env python3
"""
本地 Claude Code 工作节点
把本地 Claude Code CLI（claude -p，非交互模式）包装成 HTTP 服务，
供中枢大脑（multi_bot_manager）调度，走 Claude Pro 订阅，不额外计 API 费用。

只能在装了 Claude Code CLI 并已用 claude.ai 账号登录的机器上运行（比如 Windows 本地）。
"""

import json
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8011
CLAUDE_TIMEOUT_SECONDS = 300


def call_local_claude(prompt: str, cwd: str = None) -> dict:
    """调用本地 claude -p，返回文本结果"""
    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=CLAUDE_TIMEOUT_SECONDS,
            cwd=cwd,
        )
        if result.returncode != 0:
            return {"error": f"claude exited with code {result.returncode}: {result.stderr.strip()}"}
        return {"reply": result.stdout.strip()}
    except FileNotFoundError:
        return {"error": "claude 命令未找到，请确认已安装 Claude Code CLI 并配置好 PATH"}
    except subprocess.TimeoutExpired:
        return {"error": f"调用超时（超过 {CLAUDE_TIMEOUT_SECONDS} 秒）"}


class LocalClaudeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {
                "bot": "local-claude",
                "name": "本地 Claude Code 工作节点",
                "port": PORT,
                "status": "running",
                "billing": "claude-pro-subscription",
            }
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/task":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode())
                prompt = data.get("prompt", "")
                cwd = data.get("cwd")

                if not prompt:
                    raise ValueError("prompt 不能为空")

                result = call_local_claude(prompt, cwd=cwd)

                self.send_response(200 if "reply" in result else 502)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass


def main():
    server = HTTPServer(("0.0.0.0", PORT), LocalClaudeHandler)
    print(f"🤖 本地 Claude Code 工作节点已启动 (端口 {PORT})")
    print(f"   POST http://localhost:{PORT}/task   {{\"prompt\": \"任务内容\", \"cwd\": \"可选工作目录\"}}")
    print("   走 Claude Pro 订阅计费，不额外消耗 API 余额\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 已停止")


if __name__ == "__main__":
    main()
