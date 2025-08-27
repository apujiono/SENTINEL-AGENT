# agent-mini.py
import time
import requests
import psutil
from datetime import datetime

# 🔧 Konfigurasi (GANTI INI SESUAI HIVE-MU)
HIVE_URL = "https://sentinel-core-production.up.railway.app/?key=watcher123/alert"  # GANTI!
AGENT_ID = "agent-Ninja"                                # GANTI!
SCAN_INTERVAL = 5

def report(alert, level="info"):
    try:
        data = {
            "node": AGENT_ID,
            "alert": alert,
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "timestamp": datetime.now().isoformat(),
            "token": "rahasia"  # Bisa dipakai untuk auth
        }
        response = requests.post(HIVE_URL, json=data, timeout=5)
        if response.status_code == 200:
            print(f"🟢 Laporan dikirim: {alert}")
        else:
            print(f"🟡 Gagal kirim: {response.status_code}")
    except Exception as e:
        print(f"🔴 Error: {e}")

# 🔁 Loop utama
if __name__ == "__main__":
    print(f"🤖 Agent aktif: {AGENT_ID} → {HIVE_URL}")
    while True:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        
        # Kirim laporan rutin
        report(f"📊 CPU={cpu}%, RAM={ram}%")
        
        # Deteksi CPU tinggi
        if cpu > 80:
            report(f"🔥 CPU Tinggi: {cpu}%", "warning")
        
        time.sleep(SCAN_INTERVAL)