import network
import time

# Wi-Fi credentials
ssid     = 'NUM DIGITAL'
password = 'num@digital'

# --- Static IP configuration ---
static_ip    = '10.250.0.22' # Replace with your Desired fixed IP for the Pico W
subnet_mask  = '255.255.255.0'
gateway_ip   = '10.250.0.1'   # Your router's IP address
dns_server   = '8.8.8.8'         # Google Public DNS

# Initialize and connect
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() >= 3:
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)

# Apply the static IP configuration
wlan.ifconfig((static_ip, subnet_mask, gateway_ip, dns_server))

if wlan.status() != 3:
    raise RuntimeError('Failed to establish a network connection')
else:
    print('Connection successful!')
    network_info = wlan.ifconfig()
    print('IP address:', network_info[0])
