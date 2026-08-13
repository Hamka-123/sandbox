
from http.server import HTTPServer, SimpleHTTPRequestHandler

HOST = '0.0.0.0'
PORT = 9999
server = HTTPServer((HOST,PORT), SimpleHTTPRequestHandler)
print(f'HTTP server listening on {HOST=} . {PORT=}')
server.serve_forever()