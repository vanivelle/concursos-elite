#!/usr/bin/env python3
"""
Simple HTTP Proxy/Tunnel - Expõe localhost:8000 para internet
Usa WebSocket ou HTTP passthrough simples
"""
import http.server
import socketserver
import threading
import requests
import json
from urllib.parse import urljoin

LOCAL_PORT = 9000
BACKEND_URL = "http://localhost:8000"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Proxy GET requests"""
        try:
            url = urljoin(BACKEND_URL, self.path)
            headers = dict(self.headers)
            headers.pop('Host', None)
            
            resp = requests.get(url, headers=headers, timeout=10)
            
            self.send_response(resp.status_code)
            for key, val in resp.headers.items():
                if key.lower() not in ['content-encoding', 'transfer-encoding']:
                    self.send_header(key, val)
            self.end_headers()
            self.wfile.write(resp.content)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_POST(self):
        """Proxy POST requests"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            url = urljoin(BACKEND_URL, self.path)
            headers = dict(self.headers)
            headers.pop('Host', None)
            
            resp = requests.post(url, data=body, headers=headers, timeout=10)
            
            self.send_response(resp.status_code)
            for key, val in resp.headers.items():
                if key.lower() not in ['content-encoding', 'transfer-encoding']:
                    self.send_header(key, val)
            self.end_headers()
            self.wfile.write(resp.content)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def log_message(self, format, *args):
        """Log requests"""
        print(f"[PROXY] {format % args}")

if __name__ == "__main__":
    handler = ProxyHandler
    with socketserver.TCPServer(("", LOCAL_PORT), handler) as httpd:
        print(f"✅ Proxy iniciado na porta {LOCAL_PORT}")
        print(f"📍 Local Backend: {BACKEND_URL}")
        print(f"🌐 Para expor, use em outro terminal:")
        print(f"   ssh -R 80:localhost:{LOCAL_PORT} ssh.localhost.run")
        print(f"\n⏹️  Pressione CTRL+C para parar")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n❌ Proxy parado")
