from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import xml.etree.ElementTree as ET

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # HTML içeriği buraya ekleyin
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Game Code Redemption</title>
            </head>
            <body>
                <h1>Game Code Redemption</h1>
                
                <form method="post" action="/redeem">
                    <button type="submit" name="game_id" value="1">Animal Nursery</button>
                    <button type="submit" name="game_id" value="2">Car Club</button>
                </form>

                <label for="code">Enter the numeric code:</label>
                <input type="text" id="code" name="code" required>

                <p>{result}</p>
            </body>
            </html>
            """.format(result="")

            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_params = dict(param.split('=') for param in post_data.split('&'))

        if self.path == '/redeem':
            game_id = int(post_params.get('game_id', 0))
            code = post_params.get('code', '')

            if game_id == 1:
                result = self.redeem_animal_nursery_code(code)
            elif game_id == 2:
                result = self.redeem_car_club_code(code)
            else:
                result = "Invalid selection."

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Game Code Redemption</title>
            </head>
            <body>
                <h1>Game Code Redemption</h1>
                
                <form method="post" action="/redeem">
                    <button type="submit" name="game_id" value="1">Animal Nursery</button>
                    <button type="submit" name="game_id" value="2">Car Club</button>
                </form>

                <label for="code">Enter the numeric code:</label>
                <input type="text" id="code" name="code" required>

                <p>{result}</p>
            </body>
            </html>
            """.format(result=result)

            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_error(404, 'Not Found')

    def redeem_animal_nursery_code(self, code):
        # Burada gerçek redemption mantığınızı ekleyin
        xml_data = requests.get("https://vodafonecarclub.apphicgames.com/WebService1.asmx/Use_Code_AnimalNursery?code="+code+"&pin=app2022?*1", verify=False).text
        root = ET.fromstring(xml_data)
        result = root.text

        if result == "2":
            return "[+] 2GB Alındı"
        elif result == "1":
            return "[*] Kodu Zaten Kullanmışsın"
        elif result == "0":
            return "[!] Yanlış Kod veya Yanlış oyun Seçtin"
        else:
            return "[x] Bir Sorun oluştu"

    def redeem_car_club_code(self, code):
        # Burada gerçek redemption mantığınızı ekleyin
        xml_data = requests.get("https://vodafonecarclub.apphicgames.com/WebService1.asmx/Use_Code_CarRacing?code="+code+"&pin=app2022?*1", verify=False).text
        root = ET.fromstring(xml_data)
        result = root.text

        if result == "2":
            return "[+] 2GB Alındı"
        elif result == "1":
            return "[*] Kodu Zaten Kullanmışsın"
        elif result == "0":
            return "[!] Yanlış Kod veya Yanlış oyun Seçtin"
        else:
            return "[x] Bir Sorun oluştu"

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('localhost', port), RequestHandler)
    print(f'Server started on http://localhost:{port}')
    server.serve_forever()
