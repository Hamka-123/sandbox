from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # Получаем ID контейнера из переменной окружения HOSTNAME
        container_id = os.environ.get('HOSTNAME', 'unknown')
        html = f"<html><body><h1>Hello!</h1><p>I am container: <b>{container_id}</b></p></body></html>"
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    print("Starting Python server on port 8888...")
    web_server = HTTPServer(("0.0.0.0", 8888), MyServer)
    web_server.serve_forever()