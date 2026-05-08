import network
import socket
import time
from machine import Pin

# ==========================================
# Wi-Fi Configuration
# ==========================================

SSID = "NUM DIGITAL"
PASSWORD = "num@digital"

AP_SSID = "14_Srun_Sochettra"
AP_PASSWORD = "12345678"

CONNECTION_TIMEOUT = 10

# ==========================================
# LED Setup
# ==========================================

led = Pin("LED", Pin.OUT)

# ==========================================
# STA Interface
# ==========================================

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# ==========================================
# AP Interface
# ==========================================

ap = network.WLAN(network.AP_IF)

# ==========================================
# Connect to Wi-Fi
# ==========================================

def connect_sta():

    print("Connecting to Wi-Fi...")
    
    wlan.connect(SSID, PASSWORD)

    timeout = CONNECTION_TIMEOUT

    while timeout > 0:

        status = wlan.status()

        if status >= 3:
            break

        print("Waiting for connection...")
        timeout -= 1
        time.sleep(1)

    if wlan.isconnected():

        ip = wlan.ifconfig()[0]

        print("\n✅ STA MODE ACTIVE")
        print("Connected to:", SSID)
        print("IP Address:", ip)

        return ip

    else:
        print("\n❌ STA connection failed")

        return None

# ==========================================
# Start Access Point
# ==========================================

def start_ap():

    ap.active(True)

    ap.config(
        essid=AP_SSID,
        password=AP_PASSWORD
    )

    ip = ap.ifconfig()[0]

    print("\n📡 AP MODE ACTIVE")
    print("SSID:", AP_SSID)
    print("Password:", AP_PASSWORD)
    print("AP IP Address:", ip)

    return ip

# ==========================================
# Web Page
# ==========================================

def webpage():

    led_state = "ON" if led.value() else "OFF"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pico W Hybrid IoT</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>
            body {{
                font-family: Arial;
                text-align: center;
                margin-top: 40px;
                background-color: #f2f2f2;
            }}

            h1 {{
                color: #333;
            }}

            .card {{
                background: white;
                padding: 20px;
                margin: auto;
                width: 300px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
            }}

            button {{
                width: 120px;
                height: 50px;
                font-size: 18px;
                margin: 10px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }}

            .on {{
                background-color: green;
                color: white;
            }}

            .off {{
                background-color: red;
                color: white;
            }}
        </style>
    </head>

    <body>

        <div class="card">

            <h1>Pico W Hybrid IoT</h1>

            <p><b>LED State:</b> {led_state}</p>

            <a href="/led/on">
                <button class="on">LED ON</button>
            </a>

            <a href="/led/off">
                <button class="off">LED OFF</button>
            </a>

        </div>

    </body>
    </html>
    """

    return html

# ==========================================
# Start Server
# ==========================================

def start_server(ip):

    addr = socket.getaddrinfo(ip, 80)[0][-1]

    server = socket.socket()

    server.bind(addr)

    server.listen(1)

    print("\n🌐 Web Server Running")
    print("Open browser:", "http://" + ip)

    while True:

        client, addr = server.accept()

        print("Client connected:", addr)

        request = client.recv(1024)

        request = str(request)

        # ------------------------------
        # LED ON
        # ------------------------------
        if "/led/on" in request:
            led.value(1)

        # ------------------------------
        # LED OFF
        # ------------------------------
        if "/led/off" in request:
            led.value(0)

        response = webpage()

        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: text/html\r\n")
        client.send("Connection: close\r\n\r\n")
        client.sendall(response)

        client.close()

# ==========================================
# MAIN PROGRAM
# ==========================================

ip = connect_sta()

# If STA fails -> Start AP
if ip is None:
    ip = start_ap()

# Start Web Server
start_server(ip)