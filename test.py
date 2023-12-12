from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import urllib.parse
import requests
import xml.etree.ElementTree as ET

class Handler(BaseHTTPRequestHandler):
    def _set_response(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            with open('indexx.html', 'rb') as file:
                self._set_response()
                self.wfile.write(file.read())
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_params = urllib.parse.parse_qs(post_data.decode('utf-8'))

        if self.path == '/animal_nursery':
            kod = post_params['animal_nursery_kod'][0]
            sonuc = self.use_code_animal_nursery(kod)
            self._set_response()
            self.wfile.write(sonuc.encode('utf-8'))

        elif self.path == '/car_club':
            kod = post_params['car_club_kod'][0]
            sonuc = self.use_code_car_club(kod)
            self._set_response()
            self.wfile.write(sonuc.encode('utf-8'))

        else:
            self.send_error(404)

    def use_code_animal_nursery(self, kod):
        xml_data = requests.get("https://vodafonecarclub.apphicgames.com/WebService1.asmx/Use_Code_AnimalNursery?code="+kod+"&pin=app2022?*1", verify=False).text
        dark = ET.fromstring(xml_data)
        sonuc = dark.text
        if sonuc == "2":
            return "[+] 2GB Alındı"
        elif sonuc == "1":
            return "[*] Kodu Zaten Kullanmışsın"
        elif sonuc == "0":
            return "[!] Yanlış Kod veya Yanlış oyun Seçtin"
        else:
            return "[x] Bir Sorun oluştu"

    def use_code_car_club(self, kod):
        xml_data = requests.get("https://vodafonecarclub.apphicgames.com/WebService1.asmx/Use_Code_CarRacing?code="+kod+"&pin=app2022?*1", verify=False).text
        dark = ET.fromstring(xml_data)
        sonuc = dark.text
        if sonuc == "2":
            return "[+] 2GB Alındı"
        elif sonuc == "1":
            return "[*] Kodu Zaten Kullanmışsın"
        elif sonuc == "0":
            return "[!] Yanlış Kod veya Yanlış oyun Seçtin"
        else:
            return "[x] Bir Sorun oluştu"

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run_server(server_class=ThreadedHTTPServer, handler_class=Handler, port=3169):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Sunucu {port} portunda ...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
