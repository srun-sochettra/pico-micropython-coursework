import network
import time

ap = network.WLAN(network.AP_IF)
ap.active(True)

ap.config(essid='14_Srun_Sochettra', password='12345678')

print("Starting AP...")

time.sleep(2)

if ap.active():
    print("✅ AP is active")
    print("📡 SSID:", ap.config('essid'))
    print("🌐 IP:", ap.ifconfig()[0])
else:
    print("❌ Failed to start AP")