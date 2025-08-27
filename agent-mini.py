# agent-mini.py
import time
import requests
import psutil
from datetime import datetime
import os

# 🔧 KONFIGURASI (GANTI SESUAI HIVE-MU)
HIVE_URL = "https://https://sentinel-core-production.up.railway.app/?key=watcher123"  # GANTI INI
DASH_KEY = "watcher123"  # HARUS SAMA DENGAN DI HIVE
AGENT_ID = f"railway-agent-{os.getenv('RAILWAY_RELEASE_ID', 'local')}"
SCAN_INTERVAL = 30  # Railway sleep, jadi jangan terlalu cepat

def report(alert, level="info"):
    try:
        data = {
            "node": AGENT_ID,
            "alert": alert,
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "timestamp": datetime.now().isoformat()
        }
        # ✅ Kirim key di URL
        response = requests.post(
            f"{HIVE_URL}?key={DASH_KEY}",
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            print(f"🟢 Laporan dikirim: {alert}")
        else:
            print(f"❌ Gagal kirim: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"🔴 Error: {e}")

# 🔁 Loop utama
if __name__ == "__main__":
    print(f"🤖 Agent aktif: {AGENT_ID}")
    while True:
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            report(f"📊 CPU={cpu}%, RAM={ram}%")
            if cpu > 80:
                report(f"🔥 CPU Tinggi: {cpu}%", "warning")
        except Exception as e:
            print(f"⚠️ Error di loop: {e}")
        time.sleep(SCAN_INTERVAL)