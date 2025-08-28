# agent-mini.py
import time
import requests
import psutil
from datetime import datetime
import os

# 🔧 KONFIGURASI
HIVE_URL = "https://sentinel-core-production.up.railway.app/alert"
DASH_KEY = "watcher123"  # Pastikan sama dengan di Hive
AGENT_ID = f"railway-agent-{os.getenv('RAILWAY_RELEASE_ID', 'local')}"
SCAN_INTERVAL = 30
TIMEOUT = 30  # Diperpanjang dari 10 → 30 detik
MAX_RETRIES = 3  # Coba ulang 3 kali jika gagal

def report(alert, level="info"):
    data = {
        "node": AGENT_ID,
        "alert": alert,
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "timestamp": datetime.now().isoformat()
    }

    for attempt in range(MAX_RETRIES):
        try:
            print(f"📡 Mencoba kirim ke Hive (percobaan {attempt+1})...")
            response = requests.post(
                f"{HIVE_URL}?key={DASH_KEY}",
                json=data,
                timeout=TIMEOUT
            )
            if response.status_code == 200:
                print(f"🟢 Laporan dikirim: {alert}")
                return  # Berhasil → keluar
            else:
                print(f"🟡 Gagal: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout (percobaan {attempt+1})")
        except requests.exceptions.ConnectionError as e:
            print(f"🔌 Koneksi gagal: {e}")
        except Exception as e:
            print(f"❌ Error tak terduga: {e}")

        # Tunggu sebelum coba lagi
        if attempt < MAX_RETRIES - 1:
            time.sleep(10)

    print("🔴 Semua percobaan gagal. Menunggu interval berikutnya...")

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