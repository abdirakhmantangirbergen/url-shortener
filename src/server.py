import json
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

url_db = {}

class ShortenerHandler(BaseHTTPRequestHandler):
    def _send_response(self, status, content_type, body):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/':
            self._send_response(200, 'application/json', b'{"message": "URL Shortener API is running"}')
        elif self.path == '/healthz':
            self._send_response(200, 'application/json', b'{"status": "ok"}')
        else:
            short_id = self.path.lstrip('/')
            if short_id in url_db:
                self.send_response(307)
                self.send_header('Location', url_db[short_id])
                self.end_headers()
            else:
                self._send_response(404, 'application/json', b'{"error": "Not found"}')

    def do_POST(self):
        if self.path == '/shorten':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                original_url = data.get('url')
                if not original_url:
                    self._send_response(400, 'application/json', b'{"error": "Missing url"}')
                    return
                short_id = hashlib.sha256(original_url.encode()).hexdigest()[:6]
                url_db[short_id] = original_url
                resp = json.dumps({"short_id": short_id, "original_url": original_url})
                self._send_response(200, 'application/json', resp.encode('utf-8'))
            except json.JSONDecodeError:
                self._send_response(400, 'application/json', b'{"error": "Invalid JSON"}')
        else:
            self._send_response(404, 'application/json', b'{"error": "Not found"}')

def run(server_class=HTTPServer, handler_class=ShortenerHandler):
    port = int(os.environ.get('PORT', 8080))
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
