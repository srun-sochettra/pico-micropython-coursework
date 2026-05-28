# main.py  –  Synchronous Pico 2W Web Server
import network, socket, time, random
from machine import Pin

# ── Wi-Fi credentials ──────────────────────────────────────────
from secrets import SSID, PASSWORD

# ── Hardware ───────────────────────────────────────────────────
led = Pin("LED", Pin.OUT)  # onboard LED on Pico W

# ── HTML template ──────────────────────────────────────────────
HTML = """<!DOCTYPE html>
<html><head><title>Pico 2W</title>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<style>
  body{{font-family:Arial,sans-serif;text-align:center;padding:20px}}
  h1{{color:#006480}} h2{{color:#E05A00}}
  button{{padding:14px 28px;font-size:18px;margin:8px;border:none;
          border-radius:8px;cursor:pointer;color:white}}
  .on{{background:#4CAF50}} .off{{background:#F44336}}
  .val{{background:#2196F3}}
</style></head><body>
<h1>Pico 2W Web Server</h1>
<h2>LED Control</h2>
<a href='./lighton'><button class='on'>Turn ON</button></a>
<a href='./lightoff'><button class='off'>Turn OFF</button></a>
<p>LED state: <strong>{state}</strong></p>
<h2>Sensor Value</h2>
<a href='./value'><button class='val'>Fetch Value</button></a>
<p>Value: <strong>{value}</strong></p>
</body></html>"""

# ── Connect to Wi-Fi ──────────────────────────────────────────
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print(f"\n🔌 Connecting to Wi-Fi: {SSID}", end="")
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print(".", end="")  # Print one dot every second
    time.sleep(0.5)
# Check connection result
if wlan.isconnected():
    print(f"\n📡 Wi-Fi: {SSID}", end="")
    print(" ✅ Connected Successfully!")
    ip = wlan.ifconfig()[0]
    print("Server running at http://" + ip)

# ── Set up socket ──────────────────────────────────────────────
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)

# ── State variables ────────────────────────────────────────────
led_state = "OFF"
value = 0

# ── Request handling loop ──────────────────────────────────────
while True:
    conn, client_addr = s.accept()
    request = str(conn.recv(1024))
    print("Client:", client_addr, "| Request:", request[:50])

    if "GET /lighton" in request:
        led.on()
        led_state = "ON"
    elif "GET /lightoff" in request:
        led.off()
        led_state = "OFF"
    elif "GET /value" in request:
        value = random.randint(0, 100)  # replace with sensor read

    # Build and send HTTP response
    body = HTML.format(state=led_state, value=value)
    headers = (
        "HTTP/1.0 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "Content-Length: {}\r\n\r\n"
    ).format(len(body))
    conn.send(headers)
    conn.send(body)
    conn.close()
