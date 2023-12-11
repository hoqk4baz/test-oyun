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
            self.wfile.write(self.generate_html().encode('utf-8'))
        else:
            self.send_error(404)

    def generate_html(self):
        return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Code by ☬𝐃𝐀𝐑𝐊 | 𝐄𝐍𝐙𝐀☬</title>
                <style>
                    body {
                        background-color: #222;
                        color: #fff;
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100vh;
                    }
                    .container {
                        background-color: #333;
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                    }
                    button {
                        background-color: #800080; /* Mor Renk */
                        color: white;
                        padding: 10px 15px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        margin-top: 10px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>İlgi ve Alakanız İçin Teşekkürler!</h1>
                    <p>Fazla yayıldığı için sistemi kapatıyorum.</p>
                    <button onclick="redirectToTelegram()">TG Kanalı</button>
                </div>

                <script>
                    function redirectToTelegram() {
                        window.location.href = 'https://t.me/+oPB5lx8PtLxmNWI0';
                    }
                </script>
            </body>
            </html>
        """

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run_server(server_class=ThreadedHTTPServer, handler_class=Handler, port=3169):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Sunucu {port} portunda Çalışıyor...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
