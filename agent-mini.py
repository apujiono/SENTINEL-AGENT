# agent-mini.py
import time
import requests
import psutil
from datetime import datetime
import os

# 🔐 Ambil key dari environment
DASH_KEY = os.getenv('DASH_KEY', 'watcher123')
HIVE_URL = os.getenv('HIVE_URL', 'https://sentinel-core-production.up.railway.app/alert')
AGENT_ID = f"agent-{os.getenv('RAILWAY_RELEASE_ID', 'local')}"

def report(alert, level="info"):
    data = {
        "node": AGENT_ID,
        "alert": alert,
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "timestamp": datetime.now().isoformat()
    }
    try:
        # Kirim key di URL
        response = requests.post(
            f"{HIVE_URL}?key={DASH_KEY}",
            json=data,
            timeout=30
        )
        if response.status_code == 200:
            print(f"🟢 Laporan dikirim: {alert}")
        else:
            print(f"❌ Gagal: {response.status_code}")
    except Exception as e:
        print(f"🔴 Error: {e}")

if __name__ == "__main__":
    print(f"🤖 Agent aktif: {AGENT_ID}")
    while True:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        report(f"📊 CPU={cpu}%, RAM={ram}%")
        time.sleep(30)