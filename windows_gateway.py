from http.server import HTTPServer, BaseHTTPRequestHandler
import json, threading

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            resp = {"status": "ok", "gateway": "openclaw-windows", "port": 9000}
            self.wfile.write(json.dumps(resp).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, *args):
        pass

server = HTTPServer(('127.0.0.1', 9000), Handler)
print('Windows Gateway 启动: http://localhost:9000')
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('\n关闭')
