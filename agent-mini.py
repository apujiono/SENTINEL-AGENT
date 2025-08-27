# agent-mini.py (versi Flask)
from flask import Flask
import time
import requests
import psutil
from datetime import datetime
import threading

app = Flask(__name__)

HIVE_URL = "https://sentinel-core-production.up.railway.app/alert"
AGENT_ID = "flask-agent-railway"

def background_task():
    while True:
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            data = {
                "node": AGENT_ID,
                "alert": f"📊 CPU={cpu}%, RAM={ram}%",
                "cpu": cpu,
                "ram": ram,
                "timestamp": datetime.now().isoformat()
            }
            requests.post(HIVE_URL, json=data, timeout=5)
            print(f"🟢 Laporan dikirim: CPU={cpu}%, RAM={ram}%")
        except:
            print("🔴 Gagal kirim laporan")
        time.sleep(30)

@app.route('/')
def home():
    return "🤖 Sentinel Agent Mini Aktif", 200

# Jalankan background task
thread = threading.Thread(target=background_task)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)