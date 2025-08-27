# agent-mini.py
import time
import requests
import psutil
from datetime import datetime
import os

# 🔧 KONFIGURASI (GANTI INI)
HIVE_URL = "https://https://sentinel-core-production.up.railway.app/alert"  # GANTI DENGAN HIVE-MU
AGENT_ID = f"railway-agent-{os.getenv('RAILWAY_RELEASE_ID', 'local')}"  # ID unik
SCAN_INTERVAL = 10  # Railway sleep setiap 30 detik, jadi jangan terlalu cepat

def report(alert, level="info"):
    try:
        data = {
            "node": AGENT_ID,
            "alert": alert,
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "timestamp": datetime.now().isoformat(),
            "platform": "railway"
        }
        # Tambahkan timeout lebih lama
        response = requests.post(HIVE_URL, json=data, timeout=10)
        if response.status_code == 200:
            print(f"🟢 Laporan dikirim: {alert}")
        else:
            print(f"🟡 Gagal kirim (status {response.status_code}): {response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"🔴 Koneksi gagal: {e}")
    except requests.exceptions.Timeout as e:
        print(f"⏰ Timeout: {e}")
    except Exception as e:
        print(f"❌ Error tak terduga: {e}")

# 🔁 Loop utama
if __name__ == "__main__":
    print(f"🤖 Agent aktif: {AGENT_ID} → {HIVE_URL}")
    while True:
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent

            # Kirim laporan
            report(f"📊 CPU={cpu}%, RAM={ram}%")

            # Deteksi CPU tinggi
            if cpu > 80:
                report(f"🔥 CPU Tinggi: {cpu}%", "warning")

        except Exception as e:
            print(f"⚠️ Error di loop: {e}")

        time.sleep(SCAN_INTERVAL)