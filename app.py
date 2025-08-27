import time
import requests
import psutil
from datetime import datetime

HIVE_URL = "https://sentinel-core-production.up.railway.app/?key=watcher123/>
NODE_ID = "agent-NinjaRail"

def report(alert):
    try:
        data = {
            "node": NODE_ID,
            "alert": alert,
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percen>
            "time": datetime.now().strftime("%H:%>
        }
        requests.post(HIVE_URL, json=data, timeou>
        print(f"🟢 Lapor: {alert}")
except Exception as e:
        print(f"🔴 Gagal: {e}")

while True:
    cpu = psutil.cpu_percent()
    if cpu > 80:
        report(f"🔥 CPU Tinggi: {cpu}%")
    time.sleep(10)
