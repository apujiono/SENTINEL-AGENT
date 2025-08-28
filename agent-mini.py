# agent-mini.py
import time
import requests
import os
from datetime import datetime

HIVE_URL = os.getenv('HIVE_URL', 'https://sentinel-core-production.up.railway.app')
DASH_KEY = os.getenv('DASH_KEY', 'watcher123')
AGENT_ID = f"railway-{os.getenv('RAILWAY_RELEASE_ID', 'local')}-{int(time.time()) % 10000}"

def report(alert):
    data = {
        "node": AGENT_ID,
        "alert": alert,
        "timestamp": datetime.now().isoformat()
    }
    try:
        requests.post(f"{HIVE_URL}/alert?key={DASH_KEY}", json=data, timeout=30)
        print(f"🟢 Laporan dikirim: {alert}")
    except Exception as e:
        print(f"🔴 Gagal: {e}")

if __name__ == "__main__":
    print(f"🤖 Agent aktif: {AGENT_ID}")
    while True:
        report("Laporan rutin")
        time.sleep(30)