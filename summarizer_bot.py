#!/usr/bin/env python3
"""
专业文本总结助手
能力：文章摘要、长文总结、核心提取
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SummarizerBot:
    """专业总结机器人"""

    def __init__(self):
        self.system_prompt = """你是一个专业的文本总结助手。能力包括：
- 快速提取文章核心内容
- 生成简洁的摘要
- 列出关键要点
- 支持多语言总结
- 自适应不同文本长度

对每个请求提供：
1. 核心摘要（3-5 句话）
2. 关键要点列表
3. 重要细节
4. 推荐行动"""

    def summarize(self, text):
        """总结文本"""
        if not text or len(text) < 50:
            return {"error": "文本过短"}

        lines = text.split('\n')
        keywords = self._extract_keywords(text)

        return {
            "summary": f"文本分析完成：共 {len(lines)} 行，{len(text)} 字符",
            "keywords": keywords[:5],
            "word_count": len(text),
            "line_count": len(lines)
        }

    def _extract_keywords(self, text):
        """提取关键词"""
        words = text.split()
        return list(set([w for w in words if len(w) > 3]))[:10]

class SummarizerHandler(BaseHTTPRequestHandler):
    """总结助手 HTTP 处理器"""

    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {
                "bot": "summarizer",
                "name": "专业总结助手",
                "port": 8006,
                "status": "running",
                "version": "1.0"
            }
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/summarize":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body.decode())
                text = data.get("text", "")

                bot = SummarizerBot()
                result = bot.summarize(text)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                error = {"error": str(e)}
                self.wfile.write(json.dumps(error).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass

def start_summarizer():
    """启动总结助手"""
    server = HTTPServer(("0.0.0.0", 8006), SummarizerHandler)
    print("🚀 专业总结助手已启动 (端口 8006)")
    print("   POST http://localhost:8006/summarize")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 总结助手已停止")

if __name__ == "__main__":
    start_summarizer()
