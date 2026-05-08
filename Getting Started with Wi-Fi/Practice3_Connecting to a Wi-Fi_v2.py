import network
import time

# ==============================
# Wi-Fi Configuration
# ==============================
SSID = 'NUM DIGITAL'
PASSWORD = 'num@digital'
MAX_RETRIES = 3
TIMEOUT = 10  # seconds

# ==============================
# Initialize WLAN
# ==============================
wlan = network.WLAN(network.STA_IF)
wlan.active(True)


# ==============================
# Scan Networks
# ==============================
def scan_networks():
    print("\n🔍 Scanning for Wi-Fi networks...")
    nets = wlan.scan()
    
    found = False
    for net in nets:
        ssid = net[0].decode()
        rssi = net[3]
        
        print(f"SSID: {ssid:30} | RSSI: {rssi} dBm")
        
        if ssid == SSID:
            found = True

    return found


# ==============================
# Connect to Wi-Fi
# ==============================
def connect_wifi():
    if wlan.isconnected():
        print("✅ Already connected.")
        return True

    if not scan_networks():
        print("❌ Target SSID not found!")
        return False

    print(f"\n🔌 Connecting to {SSID}...")
    wlan.connect(SSID, PASSWORD)

    timeout = TIMEOUT
    while timeout > 0:
        status = wlan.status()
        
        if status < 0:
            print("❌ Connection failed (status:", status, ")")
            return False
        elif status >= 3:
            break
        
        print("⏳ Waiting for connection...")
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("🎉 Connected successfully!")
        ip, subnet, gateway, dns = wlan.ifconfig()
        print(f"📡 IP Address : {ip}")
        print(f"🌐 Gateway    : {gateway}")
        print(f"📶 RSSI       : {wlan.status('rssi')} dBm")
        return True
    else:
        print("❌ Timeout: Failed to connect.")
        return False


# ==============================
# Auto-Retry Logic
# ==============================
def connect_with_retry():
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n🔁 Attempt {attempt}/{MAX_RETRIES}")
        
        if connect_wifi():
            return True
        
        print("⚠️ Retrying...\n")
        time.sleep(2)

    print("🚫 All connection attempts failed.")
    return False


# ==============================
# Run
# ==============================
if connect_with_retry():
    print("\n✅ System ready for IoT tasks!")
else:
    raise RuntimeError("Wi-Fi connection failed completely.")