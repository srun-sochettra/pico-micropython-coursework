import network
import socket
import time
from machine import Pin

# ==========================================
# WIFI CONFIG
# ==========================================

SSID = "NUM DIGITAL"
PASSWORD = "num@digital"

AP_SSID = "14_Srun_Sochettra"
AP_PASSWORD = "12345678"

# ==========================================
# LED SETUP
# ==========================================

led = Pin("LED", Pin.OUT)

# ==========================================
# WLAN
# ==========================================

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ap = network.WLAN(network.AP_IF)

# ==========================================
# CONNECT STA
# ==========================================

def connect_sta():

    print("Connecting to Wi-Fi...")

    wlan.connect(SSID, PASSWORD)

    timeout = 10

    while timeout > 0:

        if wlan.status() >= 3:
            break

        timeout -= 1
        print("Waiting...")
        time.sleep(1)

    if wlan.isconnected():

        ip = wlan.ifconfig()[0]

        print("\n✅ STA MODE")
        print("IP:", ip)

        return ip, "STA"

    return None, None

# ==========================================
# START AP
# ==========================================

def start_ap():

    ap.active(True)

    ap.config(
        essid=AP_SSID,
        password=AP_PASSWORD
    )

    ip = ap.ifconfig()[0]

    print("\n📡 AP MODE")
    print("SSID:", AP_SSID)
    print("IP:", ip)

    return ip, "AP"

# ==========================================
# WEB PAGE
# ==========================================

def webpage(ip, mode):

    html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>Pico W IoT Dashboard</title>

<style>

body {{
    margin: 0;
    padding: 20px;
    font-family: Arial;
    background: #f0f2f5;
}}

.container {{
    max-width: 420px;
    margin: auto;
}}

.card {{
    background: white;
    border-radius: 25px;
    padding: 25px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}}

h1 {{
    text-align: center;
    color: #333;
}}

.info {{
    font-size: 22px;
    margin: 18px 0;
}}

.label {{
    font-weight: bold;
}}

.center {{
    text-align: center;
    margin-top: 30px;
}}

.switch {{
    position: relative;
    display: inline-block;
    width: 90px;
    height: 50px;
}}

.switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.slider {{
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 50px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 38px;
    width: 38px;
    left: 6px;
    bottom: 6px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}}

input:checked + .slider {{
    background-color: #4CAF50;
}}

input:checked + .slider:before {{
    transform: translateX(40px);
}}

.status {{
    text-align: center;
    font-size: 28px;
    margin-top: 20px;
    font-weight: bold;
}}

.online {{
    color: green;
}}

.offline {{
    color: red;
}}

</style>

</head>

<body>

<div class="container">

<div class="card">

<h1>🚀 Pico W IoT</h1>

<div class="info">
<span class="label">Mode:</span>
<span id="mode">{mode}</span>
</div>

<div class="info">
<span class="label">IP:</span>
<span id="ip">{ip}</span>
</div>

<div class="status">
LED:
<span id="ledText">OFF</span>
</div>

<div class="center">

<label class="switch">

<input type="checkbox" id="toggle">

<span class="slider"></span>

</label>

</div>

</div>

</div>

<script>

const toggle = document.getElementById("toggle");
const ledText = document.getElementById("ledText");

// ======================================
// TOGGLE EVENT
// ======================================

toggle.addEventListener("change", function() {{

    let state = this.checked ? "on" : "off";

    fetch("/led?state=" + state)
    .then(response => response.text())
    .then(data => {{
        updateUI(data);
    }});

}});

// ======================================
// UPDATE UI
// ======================================

function updateUI(state) {{

    if(state == "ON") {{

        toggle.checked = true;
        ledText.innerHTML = "ON";
        ledText.className = "online";

    }}

    else {{

        toggle.checked = false;
        ledText.innerHTML = "OFF";
        ledText.className = "offline";

    }}
}}

// ======================================
// REAL-TIME SYNC
// ======================================

function syncStatus() {{

    fetch("/status")
    .then(response => response.text())
    .then(data => {{
        updateUI(data);
    }});

}}

setInterval(syncStatus, 500);

// Initial sync
syncStatus();

</script>

</body>
</html>
"""

    return html

# ==========================================
# SERVER
# ==========================================

def start_server(ip, mode):

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    server = socket.socket()

    # ✅ FIX: Reuse address to prevent EADDRINUSE
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(addr)

    server.listen(5)

    print("\n🌐 SERVER RUNNING")
    print("Open:", "http://" + ip)

    while True:

        client, addr = server.accept()

        request = client.recv(1024)

        request = request.decode('utf-8')

        request_line = request.split('\r\n')[0]

        print(request_line)

        # ==================================
        # LED ON
        # ==================================

        if "GET /led?state=on" in request_line:

            led.value(1)

            response = "ON"

            client.send("HTTP/1.1 200 OK\r\n")
            client.send("Content-Type: text/plain\r\n")
            client.send("Connection: close\r\n\r\n")

            client.sendall(response.encode())

            client.close()

            continue

        # ==================================
        # LED OFF
        # ==================================

        if "GET /led?state=off" in request_line:

            led.value(0)

            response = "OFF"

            client.send("HTTP/1.1 200 OK\r\n")
            client.send("Content-Type: text/plain\r\n")
            client.send("Connection: close\r\n\r\n")

            client.sendall(response.encode())

            client.close()

            continue

        # ==================================
        # STATUS API
        # ==================================

        if "GET /status" in request_line:

            response = "ON" if led.value() else "OFF"

            client.send("HTTP/1.1 200 OK\r\n")
            client.send("Content-Type: text/plain\r\n")
            client.send("Cache-Control: no-cache\r\n")
            client.send("Connection: close\r\n\r\n")

            client.sendall(response.encode())

            client.close()

            continue

        # ==================================
        # MAIN PAGE
        # ==================================

        response = webpage(ip, mode)

        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: text/html; charset=UTF-8\r\n")
        client.send("Connection: close\r\n\r\n")

        client.sendall(response.encode('utf-8'))

        client.close()

# ==========================================
# MAIN
# ==========================================

ip, mode = connect_sta()

if ip is None:
    ip, mode = start_ap()

start_server(ip, mode)