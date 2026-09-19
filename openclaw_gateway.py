#!/usr/bin/env python3
"""
OpenClaw Gateway Server
简单的网关代理服务
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import sys

class GatewayHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "running", "gateway": "openclaw", "mode": "linux"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """处理 POST 请求"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        response = {"success": True, "received": body.decode('utf-8', errors='ignore')}
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        """简化日志输出"""
        sys.stderr.write(f"[Gateway] {args[0]}\n")

def start_gateway(host="0.0.0.0", port=8080):
    """启动网关服务"""
    server = HTTPServer((host, port), GatewayHandler)
    print(f"🚀 OpenClaw 网关已启动")
    print(f"   地址: http://{host}:{port}")
    print(f"   状态: http://{host}:{port}/status")
    print(f"   平台: Linux (Docker/Kubernetes)")
    print(f"\n按 Ctrl+C 停止服务\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 网关已停止")
        server.shutdown()

if __name__ == "__main__":
    start_gateway()
