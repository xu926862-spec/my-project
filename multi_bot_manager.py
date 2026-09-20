#!/usr/bin/env python3
"""
多机器人管理系统
同时管理和运行多个 AI 机器人
"""

import json
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import time

class BotConfig:
    """机器人配置"""
    BOTS = {
        "assistant": {
            "name": "通用助手",
            "port": 8001,
            "file": "claude_local_bot.py",
            "desc": "闲聊、问答、对话"
        },
        "coder": {
            "name": "代码修复师",
            "port": 8002,
            "file": "code_fixer_bot.py",
            "desc": "代码审查、bug修复、优化"
        },
        "writer": {
            "name": "写作助手",
            "port": 8003,
            "file": "writer_bot.py",
            "desc": "文章生成、校对、翻译"
        },
        "analyst": {
            "name": "数据分析师",
            "port": 8004,
            "file": "analyst_bot.py",
            "desc": "数据处理、图表、分析"
        },
        "teacher": {
            "name": "教学助手",
            "port": 8005,
            "file": "teacher_bot.py",
            "desc": "课程设计、答疑、教学"
        },
        "summarizer": {
            "name": "总结助手",
            "port": 8006,
            "file": "summarizer_bot.py",
            "desc": "文章摘要、关键词提取"
        },
        "legal": {
            "name": "法律顾问",
            "port": 8007,
            "file": "legal_bot.py",
            "desc": "合同审查、法律风险评估"
        },
        "medical": {
            "name": "医疗健康助手",
            "port": 8008,
            "file": "medical_bot.py",
            "desc": "症状查询、健康建议"
        },
        "finance": {
            "name": "财务顾问",
            "port": 8009,
            "file": "finance_bot.py",
            "desc": "预算规划、投资建议"
        },
        "deepseek": {
            "name": "DeepSeek 功能助手",
            "port": 8010,
            "file": "deepseek_bot.py",
            "desc": "问答、代码、翻译（DeepSeek 驱动）"
        },
        "local_claude": {
            "name": "本地 Claude Code 工作节点",
            "port": 8011,
            "file": "local_claude_bot.py",
            "desc": "调用本地 Claude Code CLI（走 Claude Pro 订阅，不计 API 费用）"
        }
    }

class BotManager:
    """机器人管理器"""

    def __init__(self):
        self.bots = {}
        self.processes = {}
        self.status = {}

    def start_bot(self, bot_id):
        """启动单个机器人"""
        if bot_id not in BotConfig.BOTS:
            return False

        config = BotConfig.BOTS[bot_id]
        try:
            print(f"🚀 启动 {config['name']} (:{config['port']})")
            # 这里可以实现启动机器人的逻辑
            self.status[bot_id] = "running"
            return True
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            self.status[bot_id] = "error"
            return False

    def start_all(self):
        """启动所有机器人"""
        print("🚀 启动多机器人系统...\n")
        for bot_id in BotConfig.BOTS.keys():
            self.start_bot(bot_id)
            time.sleep(0.5)
        print("\n✅ 所有机器人已启动！\n")

    def get_status(self):
        """获取所有机器人状态"""
        status_info = {}
        for bot_id, config in BotConfig.BOTS.items():
            status_info[bot_id] = {
                "name": config["name"],
                "port": config["port"],
                "status": self.status.get(bot_id, "stopped"),
                "url": f"http://localhost:{config['port']}"
            }
        return status_info

class ManagerHandler(BaseHTTPRequestHandler):
    """管理中心 HTTP 处理器"""
    manager = None

    def do_GET(self):
        """处理 GET 请求"""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = self.get_dashboard()
            self.wfile.write(html.encode('utf-8'))

        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            status = {
                "system": "multi-bot-manager",
                "bots": self.manager.get_status(),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.wfile.write(json.dumps(status, ensure_ascii=False, indent=2).encode())

        elif self.path == "/bots":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            bots = {k: {"name": v["name"], "desc": v["desc"], "port": v["port"]}
                    for k, v in BotConfig.BOTS.items()}
            self.wfile.write(json.dumps(bots, ensure_ascii=False, indent=2).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def get_dashboard(self):
        """生成管理仪表板"""
        status = self.manager.get_status()
        bots_html = ""
        for bot_id, info in status.items():
            status_color = "green" if info["status"] == "running" else "red"
            bots_html += f"""
            <div style="background: #f0f0f0; padding: 10px; margin: 5px; border-radius: 5px;">
                <strong>{info['name']}</strong><br>
                状态: <span style="color: {status_color};">● {info['status']}</span><br>
                端口: {info['port']} | 地址: <code>{info['url']}</code>
            </div>
            """

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>多机器人管理系统</title>
            <style>
                body {{ font-family: Arial; margin: 20px; background: #f9f9f9; }}
                h1 {{ color: #333; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .bot {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 多机器人管理系统</h1>
                <p>共 {len(status)} 个机器人</p>
                {bots_html}
                <hr>
                <p>
                    <a href="/status">📊 状态 JSON</a> |
                    <a href="/bots">📋 机器人列表</a>
                </p>
            </div>
        </body>
        </html>
        """

    def log_message(self, *args):
        """简化日志"""
        pass

def main():
    """主函数"""
    manager = BotManager()
    ManagerHandler.manager = manager

    # 启动所有机器人
    manager.start_all()

    # 启动管理服务器
    print("🌐 启动管理中心: http://localhost:5000")
    print("📊 查看状态: http://localhost:5000/status")
    print("📋 机器人列表: http://localhost:5000/bots\n")

    server = HTTPServer(("0.0.0.0", 5000), ManagerHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 管理系统已停止")
        server.shutdown()

if __name__ == "__main__":
    main()
