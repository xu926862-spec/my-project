#!/usr/bin/env python3
"""
医疗健康助手机器人
能力：症状查询、医学信息、健康建议
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MedicalBot:
    """医疗健康助手机器人"""

    def __init__(self):
        self.system_prompt = """你是一个医疗健康信息助手。能力包括：
- 常见症状信息
- 医学概念解释
- 健康和预防建议
- 医疗资源导航
- 紧急情况识别

重要：提供信息仅供参考，不能替代医学诊断"""

    def query_symptom(self, symptom):
        """查询症状信息"""
        return {
            "symptom": symptom,
            "status": "information_provided",
            "recommendation": "如症状持续，请咨询医生",
            "urgency": "moderate"
        }

class MedicalHandler(BaseHTTPRequestHandler):
    """医疗机器人 HTTP 处理器"""

    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {
                "bot": "medical",
                "name": "医疗健康助手",
                "port": 8008,
                "status": "running"
            }
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/symptom":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body.decode())
                symptom = data.get("symptom", "")

                bot = MedicalBot()
                result = bot.query_symptom(symptom)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass

def main():
    server = HTTPServer(("0.0.0.0", 8008), MedicalHandler)
    print("🏥 医疗健康助手已启动 (端口 8008)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 医疗助手已停止")

if __name__ == "__main__":
    main()
