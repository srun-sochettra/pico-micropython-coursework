import network
import time

# SSID = 'YOUR_WIFI_NAME'
# PASSWORD = 'YOUR_WIFI_PASSWORD'

from secrets import SSID, PASSWORD

# Create Wi-Fi station interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Disconnect first if already connected (optional but recommended)
if wlan.isconnected():
    wlan.disconnect()
    time.sleep(1)

print(f"\n🔌 Connecting to Wi-Fi: {SSID}", end="")

# Start connection
wlan.connect(SSID, PASSWORD)

# Wait for connection and print dots as progress indicator
timeout = 20  # seconds
while not wlan.isconnected() and timeout > 0:
    print(".", end="")   # Print one dot every second
    time.sleep(1)
    timeout -= 1

print()  # Move to the next line after the dots

# Check connection result
if wlan.isconnected():
    print("✅ Connected Successfully!")
    print("🌐 IP Address :", wlan.ifconfig()[0])
    print("📡 Subnet Mask:", wlan.ifconfig()[1])
    print("🚪 Gateway    :", wlan.ifconfig()[2])
    print("🧭 DNS Server :", wlan.ifconfig()[3])
else:
    print("❌ Connection Failed!")
    print("Please check the Wi-Fi name and PASSWORD.")