#!/usr/bin/env python3
"""
财务顾问机器人
能力：预算规划、投资建议、财务分析
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class FinanceBot:
    """财务顾问机器人"""

    def __init__(self):
        self.system_prompt = """你是一个专业的财务顾问助手。能力包括：
- 个人预算规划
- 投资组合建议
- 财务风险评估
- 税务规划提示
- 退休储蓄建议

重要：仅供参考，具体投资决策请咨询持牌财务顾问"""

    def analyze_budget(self, income, expenses):
        """分析预算"""
        savings = income - expenses
        savings_rate = (savings / income * 100) if income > 0 else 0

        return {
            "income": income,
            "expenses": expenses,
            "savings": savings,
            "savings_rate": f"{savings_rate:.1f}%",
            "recommendation": "建议储蓄率不低于 20%" if savings_rate < 20 else "储蓄率良好"
        }

class FinanceHandler(BaseHTTPRequestHandler):
    """财务机器人 HTTP 处理器"""

    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {
                "bot": "finance",
                "name": "财务顾问",
                "port": 8009,
                "status": "running"
            }
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/budget":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body.decode())
                income = float(data.get("income", 0))
                expenses = float(data.get("expenses", 0))

                bot = FinanceBot()
                result = bot.analyze_budget(income, expenses)

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
    server = HTTPServer(("0.0.0.0", 8009), FinanceHandler)
    print("💰 财务顾问已启动 (端口 8009)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 财务顾问已停止")

if __name__ == "__main__":
    main()
