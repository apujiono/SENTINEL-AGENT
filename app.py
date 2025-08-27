# agent-mini.py
import time
import requests
import psutil
import os
import subprocess
from datetime import datetime
from random import choice

# 🔧 Konfigurasi
HIVE_URL = "https://sentinel-core-production.up.railway.app/alert"  # GANTI!
AGENT_ID = f"swarm-agent-{os.getenv('RAILWAY_RELEASE_ID', 'local')}"
SCAN_INTERVAL = 10
NETWORK_RANGE = "192.168.1.0/24"

# 🔁 Auto-Replication Engine
def scan_network():
    try:
        result = subprocess.run(
            ["nmap", "-sn", NETWORK_RANGE],
            capture_output=True,
            text=True,
            timeout=30
        )
        hosts = []
        for line in result.stdout.splitlines():
            if "Nmap scan report" in line:
                ip = line.split()[-1]
                if ip != get_local_ip():
                    hosts.append(ip)
        return hosts
    except:
        return []

def get_local_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "127.0.0.1"

def deploy_to_target(ip):
    try:
        # Di dunia nyata: SSH + upload agent-mini.py
        print(f"🔁 Menyebar ke {ip}")
        # Simulasi: kirim log
        report(f"🔁 Agent menyebar ke {ip}")
        return True
    except:
        return False

def self_heal():
    """Jika CPU/RAM tinggi, restart proses"""
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    if cpu > 95 or ram > 95:
        print("🔧 Self-healing: Restart agent")
        os.execv(__file__, ['python'] + sys.argv)

# 🧠 AI Sederhana: Deteksi Anomali
def detect_anomaly(cpu, ram):
    if cpu > 90:
        return f"🔥 CPU Tinggi: {cpu}%"
    if ram > 85:
        return f"MemoryWarning: {ram}%"
    return None

# 📡 Laporan ke Hive
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
        response = requests.post(HIVE_URL, json=data, timeout=10)
        if response.status_code == 200:
            print(f"🟢 Laporan dikirim: {alert}")
        else:
            print(f"🟡 Gagal kirim: {response.status_code}")
    except Exception as e:
        print(f"🔴 Error: {e}")

# 🔁 Loop Utama
if __name__ == "__main__":
    print(f"🤖 Agent aktif: {AGENT_ID}")
    while True:
        try:
            # 1. Self-Heal
            self_heal()

            # 2. Monitor
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent

            # 3. Deteksi anomali
            anomaly = detect_anomaly(cpu, ram)
            if anomaly:
                report(anomaly, "warning")

            # 4. Auto-Replication (jika di jaringan lokal)
            if "192.168" in get_local_ip():
                hosts = scan_network()
                for host in hosts:
                    deploy_to_target(host)

            # 5. Laporan rutin
            report(f"📊 CPU={cpu}%, RAM={ram}%")

        except Exception as e:
            print(f"⚠️ Error di loop: {e}")

        time.sleep(SCAN_INTERVAL)
