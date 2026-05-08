import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def scan_networks():
    print("Scanning Wi-Fi networks...\n")
    nets = wlan.scan()
    
    for net in nets:
        ssid = net[0].decode()
        rssi = net[3]
        channel = net[2]
        security = net[4]
        
        print(f"SSID: {ssid}")
        print(f"  RSSI: {rssi} dBm")
        print(f"  Channel: {channel}")
        print(f"  Security: {security}")
        print("-" * 30)

def connect_wifi(ssid, password):
    print(f"Connecting to {ssid}...")
    wlan.connect(ssid, password)

    timeout = 10
    while timeout > 0:
        if wlan.isconnected():
            break
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("Connected!")
        print("IP Address:", wlan.ifconfig()[0])
        print("Signal Strength:", wlan.status('rssi'))
    else:
        print("Failed to connect.")

# Run scan
scan_networks()

# Example connect (you must know password)
connect_wifi("NUM DIGITAL", "num@digital")

