# main_async.py – Asynchronous Pico 2W Web Server
import asyncio
import network
import random
from machine import Pin

# ──────────────────────────────────────────────────────────────
# Wi-Fi Credentials
# ──────────────────────────────────────────────────────────────
from secrets import SSID, PASSWORD

# ──────────────────────────────────────────────────────────────
# Hardware Setup
# ──────────────────────────────────────────────────────────────
led_ctrl  = Pin(19, Pin.OUT)   # Controlled from web page
led_blink = Pin(20, Pin.OUT)   # Background blinking LED

# ──────────────────────────────────────────────────────────────
# HTML Web Page Template
# ──────────────────────────────────────────────────────────────
HTML = """<!DOCTYPE html>
<html>
<head>
<title>Pico 2W Web Server</title>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<style>
  body {{font-family: Arial; text-align: center; padding: 20px;}}
  h1 {{color: #006480;}}
  h2 {{color: #E05A00;}}
  button {{
      padding: 14px 28px;
      font-size: 18px;
      margin: 8px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      color: white;
  }}
  .on  {{background: #4CAF50;}}
  .off {{background: #F44336;}}
  .val {{background: #2196F3;}}
</style>
</head>
<body>
<h1>Pico 2W Asynchronous Web Server</h1>

<h2>LED Control</h2>
<a href="/lighton"><button class="on">Turn ON</button></a>
<a href="/lightoff"><button class="off">Turn OFF</button></a>
<p>LED State: <strong>{state}</strong></p>

<h2>Sensor Value</h2>
<a href="/value"><button class="val">Fetch Value</button></a>
<p>Value: <strong>{value}</strong></p>

</body>
</html>
"""

# Global variables
led_state = 'OFF'
value = 0

# ──────────────────────────────────────────────────────────────
# Task 1: Blink LED Independently
# ──────────────────────────────────────────────────────────────
async def task_blink():
    while True:
        led_blink.toggle()
        await asyncio.sleep(0.5)

# ──────────────────────────────────────────────────────────────
# Task 2: Background Task
# ──────────────────────────────────────────────────────────────
async def task_background():
    counter = 0
    while True:
        counter += 1
        print("Background task tick:", counter)
        await asyncio.sleep(2)

# ──────────────────────────────────────────────────────────────
# Task 3: Handle HTTP Client Requests
# ──────────────────────────────────────────────────────────────
async def handle_client(reader, writer):
    global led_state, value

    try:
        request = await reader.read(1024)
        request = request.decode('utf-8')

        # Parse HTTP request
        if 'GET /lighton' in request:
            led_ctrl.on()
            led_state = 'ON'

        elif 'GET /lightoff' in request:
            led_ctrl.off()
            led_state = 'OFF'

        elif 'GET /value' in request:
            value = random.randint(0, 100)

        # Generate web page
        body = HTML.format(state=led_state, value=value)

        # HTTP response headers
        headers = (
            "HTTP/1.0 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).format(len(body))

        # Send response
        writer.write(headers.encode())
        writer.write(body.encode())

        await writer.drain()

    except Exception as e:
        print("Client error:", e)

    finally:
        writer.close()
        await writer.wait_closed()

# ──────────────────────────────────────────────────────────────
# Connect to Wi-Fi
# ──────────────────────────────────────────────────────────────
async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print("Already connected.")
        return wlan

    print(f"\n🔌 Connecting to Wi-Fi: {SSID}", end="")
    wlan.connect(SSID, PASSWORD)

    timeout = 20
    while not wlan.isconnected() and timeout > 0:
        print(".", end="")
        await asyncio.sleep(0.5)
        timeout -= 1

    print()

    if wlan.isconnected():
        print(f"📡 Wi-Fi: {SSID} ✅ Connected Successfully!")
        print("🌐 IP Address :", wlan.ifconfig()[0])
        print("📡 Subnet Mask:", wlan.ifconfig()[1])
        print("🚪 Gateway    :", wlan.ifconfig()[2])
        print("🧭 DNS Server :", wlan.ifconfig()[3])
        return wlan
    else:
        raise RuntimeError("Wi-Fi connection failed.")

# ──────────────────────────────────────────────────────────────
# Main Program
# ──────────────────────────────────────────────────────────────
async def main():
    # Connect to Wi-Fi
    
    await connect_wifi()

    # Start background tasks
    asyncio.create_task(task_blink())
    asyncio.create_task(task_background())

    # Start asynchronous web server
    await asyncio.start_server(handle_client, "0.0.0.0", 80)
    print("🌐 Async server listening on port 80")
    print("📱 Open your browser and visit the Pico's IP address.")

    # Keep the event loop running forever
    while True:
        await asyncio.sleep(1)

# Run the event loop
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n🛑 Program stopped by user.")
except Exception as e:
    print("\n❌ Error:", e)