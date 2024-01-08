
import time
import base64
import requests
import json
import xml.etree.ElementTree as ET
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
# SSL uyarısını kapatmak için bu importları ekleyin
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_ID = '27149351'
API_HASH = '2edf2bdf7cb587effd7dc089f1989cb5'
BOT_TOKEN = '6804346665:AAHe_TweRkJNOersJJHcJR43a539CTGh3uI'

app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

headers = {
    "User-Agent": "VodafoneMCare/2308211432 CFNetwork/1325.0.1 Darwin/21.1.0",
    "Content-Length": "83",
    "Connection": "keep-alive",
    "Accept-Language": "tr_TR",
    "Accept-Encoding": "gzip, deflate, br",
    "Host": "m.vodafone.com.tr",
    "Cache-Control": "no-cache",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded"
}

url = "https://m.vodafone.com.tr/maltgtwaycbu/api/"

# Durumları (states) saklamak için bir sözlük
user_states = {}



@app.on_message(filters.command("start"))
def welcome_message(client, message):
    chat_id = message.chat.id
    user = message.from_user

    # Kullanıcının durumunu 'phone' olarak güncelle
    user_states[chat_id] = {'state': 'phone', 'telno': None, 'proid': None}
    print(user.first_name)

    welcome_text = f"Hoşgeldin {user.first_name}!\n\nTelefon Numaranı Başında 0 olmadan Gir"
    client.send_message(chat_id, welcome_text)


def process_input(client, message, text):
    chat_id = message.chat.id

    # Kullanıcının durumuna göre işlem yap
    if user_states[chat_id]['state'] == 'phone':
        user_states[chat_id]['telno'] = text
        print(user_states[chat_id]['telno'])
        client.send_message(chat_id, "🔒Vodafone Şifreni Gir")
        user_states[chat_id]['state'] = 'password'
    elif user_states[chat_id]['state'] == 'password':
        parola = text
        print(parola)
        telno = user_states[chat_id]['telno']  # Telno'yu kullanıcı durumundan al
        user_states[chat_id]['state'] = 'otp'

        data = {
            "context": "e30=",
            "username": telno,
            "method": "twoFactorAuthentication",
            "password": parola
        }

        response = requests.post(url, headers=headers, data=data)
        proid = response.json().get('process_id')
        
        if proid == None:
        	print(proid)
        	client.send_message(chat_id, "🔓Hatalı Şifre veya Numara\nTekrar Kontrol et\n\n•Aşırı Şifre Deneme Durumunda'da\Bu Hata Meydana Gelebilir")
        	return welcome_message(client, message)
        else:
        	client.send_message(chat_id, "🔓Şifre Doğrulandı")
        user_states[chat_id]['proid'] = proid  # Proid'i kullanıcı durumuna ekle

        # Kullanıcıdan 4 haneli kodu iste
        time.sleep(2)
        client.send_message(chat_id, "📨SMS ile Gelen Kodu Gir")
    elif user_states[chat_id]['state'] == 'otp':
        kod = text
        proid = user_states[chat_id]['proid']  # Proid'i kullanıcı durumundan al

        veri = {
            "langId": "tr_TR",
            "clientVersion": "17.2.5",
            "reportAdvId": "0AD98FF8-C8AB-465C-9235-DDE102D738B3",
            "pbmRight": "1",
            "rememberMe": "true",
            "sid": proid,
            "otpCode": kod,
            "platformName": "iPhone"
        }

        base64_veri = base64.b64encode(json.dumps(veri).encode('utf-8'))

        data2 = {
            "context": base64_veri,
            "grant_type": "urn:vodafone:params:oauth:grant-type:two-factor",
            "code": kod,
            "method": "tokenUsing2FA",
            "process_id": proid,
            "scope": "ALL"
        }

        response2 = requests.post(url, headers=headers, data=data2)
        sonuc2 = response2.json()
        if response2.status_code == 200:
        	client.send_message(chat_id, "✅Giriş Yapıldı")
        else:
        	client.send_message(chat_id, "❌Gelen Kod Yanlış Tekrar dene")
        	return welcome_message(client, message)
        time.sleep(1)

        # Mesajı düzenle (edit) ve işlem seçeneklerini göster
        client.send_message(chat_id, "Not: Uzun Süre İşlem Yapmadığınızda\nBot'a yeniden /start Komutu Verin")
        message_text = "•Hangi işlemi yapmak istiyorsun?"
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("VF Çark", callback_data='vf_cark')],
                [InlineKeyboardButton("VF Oyun", callback_data='vf_oyun')]
            ]
        )

        # Önceki mesajı düzenle (edit)
        message.reply_text(
            message_text,
            reply_markup=reply_markup
        )

# Kullanıcının butonlara tıklamasını işlemek için
@app.on_callback_query()
def handle_callback_query(client, callback_query):
    chat_id = callback_query.message.chat.id
    data = callback_query.data

    if data == 'vf_cark':
        # VF Çark fonksiyonunu buraya ekleyin
        vf_cark(client, chat_id)
    elif data == 'vf_oyun':
        # VF Oyun fonksiyonunu buraya ekleyin
        vf_oyun(client, chat_id)

# VF Çark fonksiyonu
def vf_cark(client, chat_id):
    o_head = {
    "Accept": "application/json",
    "Language": "tr",
    "ApplicationType": "1",
    "ClientKey": "AC491770-B16A-4273-9CE7-CA790F63365E",
    "sid": user_states[chat_id]['proid'],
    "Content-Type": "application/json",
    "Content-Length": "54",
    "Host": "m.vodafone.com.tr",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/4.10.0"
    }
    cark_data = {"clientKey": "AC491770-B16A-4273-9CE7-CA790F63365E", "clientVersion": "16.8.3", "language": "tr","operatingSystem": "android"}
    cark_url = f"https://m.vodafone.com.tr/squat/getSquatMarketingProduct?sid={user_states[chat_id]['proid']}"
    al_url = f"https://m.vodafone.com.tr/squat/updateSquatMarketingProduct?sid={proid}"
    
    cark = requests.post(cark_url, headers=o_head, json=cark_data)
    
    c1 = cark.json().get("data", {}).get("name")
    c2 = cark.json().get("data", {}).get("code")
    c3 = cark.json()["data"]["interactionID"]
    c4 = cark.json()["data"]["identifier"]
    al_data = {"clientKey":"AC491770-B16A-4273-9CE7-CA790F63365E","clientVersion":"16.8.3","code":"","identifier":c4,"interactionId":c3,"language":"tr","operatingSystem":"android"}
    al = requests.post(al_url, headers=o_head, json=al_data).json()

    client.send_message(chat_id, f"✨ {c1}")

    if c2:
        client.send_message(chat_id, f"🎉 İndirim Kodu: {c2}")
    else:
        client.send_message(chat_id, "😔 İndirim Kodu Yok.")

# VF Oyun fonksiyonu
def vf_oyun(client, chat_id):
    o_head = {
    "Accept": "application/json",
    "Language": "tr",
    "ApplicationType": "1",
    "ClientKey": "AC491770-B16A-4273-9CE7-CA790F63365E",
    "sid": user_states[chat_id]['proid'],
    "Content-Type": "application/json",
    "Content-Length": "54",
    "Host": "m.vodafone.com.tr",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/4.10.0"
    }
    o_url = f"https://m.vodafone.com.tr/marketplace?method=participateCampaignBE&sid={user_states[chat_id]['proid']}"
    o_data = {"campaignID": 6873, "latitude": "0.0", "longitude": "0.0"}
    oyun = requests.post(o_url, headers=o_head, json=o_data).json().get("participateCampaign", {}).get("productData", {}).get("password")
    

    if oyun:
        xml_data = requests.get(f"https://vodafonecarclub.apphicgames.com/WebService1.asmx/Use_Code_AnimalNursery?code={oyun}&pin=app2022?*1", verify=False).text
        
        dark = ET.fromstring(xml_data)
        sonuc = dark.text

        if sonuc == "2":
            client.send_message(chat_id, "✨2GB Alındı")
        else:
            client.send_message(chat_id, "😔Kodu Zaten Kullanmışsın")
    else:
        client.send_message(chat_id, "😔VF Oyun kodu alınamadı.")



# Kullanıcının gönderdiği her mesajı işlemek için
@app.on_message(filters.text)
def handle_messages(client, message):
    chat_id = message.chat.id
    text = message.text

    # Kullanıcının durumuna göre işlem yap
    process_input(client, message, text)

app.run()
