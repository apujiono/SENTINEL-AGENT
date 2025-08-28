# agent-mini.py
import time
import requests
import os
from datetime import datetime

HIVE_URL = os.getenv('HIVE_URL', 'https://sentinel-core-production.up.railway.app')
DASH_KEY = os.getenv('DASH_KEY', 'watcher123')
AGENT_ID = f"railway-{os.getenv('RAILWAY_RELEASE_ID', 'local')}-{int(time.time()) % 10000}"

def get_cpu():
    try:
        import psutil
        return psutil.cpu_percent()
    except:
        return 0

def get_ram():
    try:
        import psutil
        return psutil.virtual_memory().percent
    except:
        return 0

def report():
    """Kirim laporan ke Hive"""
    data = {
        "id": AGENT_ID,
        "location": "Global",
        "ip": "unknown",
        "cpu": get_cpu(),
        "ram": get_ram(),
        "status": "online"
    }
    try:
        requests.post(f"{HIVE_URL}/agent?key={DASH_KEY}", json=data, timeout=10)
        print(f"🟢 Agent terdaftar: {AGENT_ID}")
    except Exception as e:
        print(f"🔴 Gagal daftar: {e}")

def get_commands():
    """Cek perintah dari Hive"""
    try:
        response = requests.get(
            f"{HIVE_URL}/agent/commands?id={AGENT_ID}",
            timeout=10
        )
        return response.json()
    except:
        return []

def execute_command(cmd):
    """Eksekusi perintah"""
    print(f"⚙️ Menjalankan perintah: {cmd}")
    if cmd == "ping":
        print("✅ Ping sukses")
    elif cmd == "restart":
        print("🔄 Restarting agent...")
        # Di dunia nyata: restart proses
    elif cmd == "self-destruct":
        print("💀 Self-destruct activated!")
        # Di dunia nyata: hapus diri
    else:
        print(f"⚠️ Perintah tidak dikenali: {cmd}")

# 🔁 Loop utama
if __name__ == "__main__":
    print(f"🤖 Agent aktif: {AGENT_ID}")
    while True:
        try:
            # Daftar ke Hive
            report()
            
            # Cek perintah
            commands = get_commands()
            for cmd in commands:
                execute_command(cmd['command'])
                
        except Exception as e:
            print(f"⚠️ Error: {e}")
            
        time.sleep(20)  # Update setiap 20 detik