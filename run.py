from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

class Handler(BaseHTTPRequestHandler):
    def _set_response(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self._set_response()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run_server(server_class=ThreadedHTTPServer, handler_class=Handler, port=3169):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Sunucu {port} portunda Calisiyor...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
