from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import secrets

# 令牌从环境变量读取；没设置就随机生成一个并打印出来，避免网关裸奔
GATEWAY_TOKEN = os.environ.get("GATEWAY_TOKEN") or secrets.token_urlsafe(24)


class Handler(BaseHTTPRequestHandler):
    def _check_auth(self):
        token = self.headers.get("X-Gateway-Token", "")
        if not secrets.compare_digest(token, GATEWAY_TOKEN):
            self.send_response(401)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "unauthorized"}).encode())
            return False
        return True

    def do_GET(self):
        if self.path == "/status":
            if not self._check_auth():
                return
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            resp = {"status": "ok", "gateway": "openclaw-windows", "port": 9000}
            self.wfile.write(json.dumps(resp).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass


server = HTTPServer(('0.0.0.0', 9000), Handler)
print('Windows Gateway started: http://localhost:9000')
print(f'Access token (X-Gateway-Token header): {GATEWAY_TOKEN}')
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('\nStopped')
