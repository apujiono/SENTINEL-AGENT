# agent-mini.py
import time
import requests
import psutil
from datetime import datetime

HIVE_URL = "https://your-sentinel.up.railway.app/alert"  # GANTI!
AGENT_ID = "agent-auto-01"                                # GANTI!
SCAN_INTERVAL = 5

def report(alert, level="info"):
    try:
        data = {
            "node": AGENT_ID,
            "alert": alert,
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "timestamp": datetime.now().isoformat()
        }
        requests.post(HIVE_URL, json=data, timeout=5)
        print(f"🟢 Lapor: {alert}")
    except Exception as e:
        print(f"🔴 Gagal: {e}")

if __name__ == "__main__":
    print(f"🤖 Agent aktif: {AGENT_ID}")
    while True:
        cpu = psutil.cpu_percent()
        report(f"📊 CPU={cpu}%")
        if cpu > 80:
            report(f"🔥 CPU Tinggi: {cpu}%", "warning")
        time.sleep(SCAN_INTERVAL)