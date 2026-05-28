# main_async.py – Asynchronous Pico 2W Web Server
# Responsive Button Layout + Adding a Status Indicator
import asyncio
import network
import random
import json
import time
from machine import Pin

# ==========================================================
# Wi-Fi Credentials
# ==========================================================
from secrets import SSID, PASSWORD

# ==========================================================
# Hardware Setup
# ==========================================================
led_ctrl = Pin(19, Pin.OUT)     # Controlled from web page
led_blink = Pin(20, Pin.OUT)    # Background blinking LED

# Initial states
led_ctrl.off()
led_blink.off()

# ==========================================================
# HTML Web Page Template
# ==========================================================
HTML = """<!DOCTYPE html>
<html>
<head>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Pico 2W Async Web Server</title>

<style>
* {{ box-sizing: border-box; }}

body {{
    font-family: Arial, sans-serif;
    max-width: 600px;
    margin: auto;
    padding: 20px;
    background: #f9f9f9;
    color: #333;
}}

h1 {{
    color: #006480;
    border-bottom: 3px solid #006480;
    padding-bottom: 10px;
    text-align: center;
}}

h2 {{
    color: #E05A00;
    margin-top: 0;
}}

.card {{
    background: white;
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}

.btn-group {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
    margin: 16px 0;
}}

button {{
    padding: 14px 32px;
    font-size: 1rem;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    color: white;
    transition: 0.2s;
}}

button:hover {{
    opacity: 0.85;
    transform: scale(1.03);
}}

.on {{
    background: #4CAF50;
}}

.off {{
    background: #F44336;
}}

.fetch {{
    background: #2196F3;
}}

.state {{
    font-size: 1.4rem;
    font-weight: bold;
}}

.on-state {{
    color: #4CAF50;
}}

.off-state {{
    color: #F44336;
}}

.value {{
    font-size: 2rem;
    font-weight: bold;
    color: #2196F3;
}}

.footer {{
    text-align: center;
    margin-top: 30px;
    font-size: 0.9rem;
    color: #777;
}}
</style>

<script>
async function updateStatus() {{
    try {{
        const response = await fetch('/api/status');
        const data = await response.json();

        // Update sensor value
        document.getElementById('sensorValue').textContent = data.value;

        // Update uptime
        document.getElementById('uptime').textContent =
            data.uptime + ' s';

        // Update LED state badge
        const ledElement =
            document.getElementById('ledState');
        ledElement.textContent = data.led;

        if (data.led === 'ON') {{
            ledElement.className =
                'state on-state';
        }} else {{
            ledElement.className =
                'state off-state';
        }}

    }} catch (err) {{
        console.log('AJAX error:', err);
    }}
}}

// Run immediately after page loads
window.onload = function() {{
    updateStatus();

    // Refresh every 3 seconds
    setInterval(updateStatus, 3000);
}};
</script>

</head>

<body>

<h1>Pico 2W Asynchronous Web Server</h1>

<div class="card">
    <h2>LED Control</h2>
    <div class="btn-group">
        <a href="/lighton"><button class="on">Turn ON</button></a>
        <a href="/lightoff"><button class="off">Turn OFF</button></a>
    </div>
    <p>LED State:
        <span id="ledState" class="state off-state">
            {led_state}
        </span>
    </p>
</div>

<div class="card">
    <h2>Sensor Value</h2>
    <div class="btn-group">
        <a href="/value"><button class="fetch">Fetch Value</button></a>
    </div>
    <p class="value" id="sensorValue">{value}</p>
</div>

<div class="card">
    <h2>System Uptime</h2>
    <p class="value" id="uptime">0 s</p>
</div>

<div class="footer">
    Powered by Raspberry Pi Pico 2 W and MicroPython
</div>

</body>
</html>
"""

# ==========================================================
# Global Variables
# ==========================================================
led_state = 'OFF'
value = 0


# ==========================================================
# Task 1: Blink LED Independently
# ==========================================================
async def task_blink():
    while True:
        led_blink.toggle()
        await asyncio.sleep(0.5)


# ==========================================================
# Task 2: Background Task
# ==========================================================
async def task_background():
    counter = 0
    while True:
        counter += 1
        print("Background task tick:", counter)
        await asyncio.sleep(2)


# ==========================================================
# Task 3: Handle HTTP Client Requests
# ==========================================================
# ==========================================================
# Route Handler Functions
# ==========================================================
def route_lighton():
    global led_state
    led_ctrl.on()
    led_state = 'ON'
    print("Action: LED ON")
    return led_state


def route_lightoff():
    global led_state
    led_ctrl.off()
    led_state = 'OFF'
    print("Action: LED OFF")
    return led_state


def route_value():
    global value
    value = random.randint(0, 100)
    print("Action: New Sensor Value =", value)
    return str(value)

# ==========================================================
# API Route: Return System Status as JSON
# ==========================================================
def route_api_status():
    data = {
        'led': led_state,
        'value': value,
        'uptime': time.ticks_ms() // 1000
    }

    print("Action: API Status Requested")
    return json.dumps(data)

# ==========================================================
# URL Routing Table
# ==========================================================
ROUTES = {
    '/lighton':     route_lighton,
    '/lightoff':    route_lightoff,
    '/value':       route_value,
    '/api/status':  route_api_status,
}


# ==========================================================
# Request Router
# ==========================================================
def handle_request(request_str):
    for path, handler in ROUTES.items():
        if ('GET ' + path) in request_str:
            print("Matched Route:", path)
            result = handler()
            return path, result

    print("Matched Route: / (default page)")
    return None, None

# ==========================================================
# Handle HTTP Client Requests
# ==========================================================
async def handle_client(reader, writer):
    global led_state, value

    try:
        # Read HTTP request
        request = await reader.read(1024)
        request = request.decode('utf-8')

        # Print first request line
        first_line = request.split('\r\n')[0]
        print("HTTP Request:", first_line)

        # Process routing
        path, result = handle_request(request)

        # --------------------------------------------------
        # JSON API Response
        # --------------------------------------------------
        if path == '/api/status':
            body = result
            headers = (
                "HTTP/1.0 200 OK\r\n"
                "Content-Type: application/json\r\n"
                "Content-Length: {}\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).format(len(body))

        # --------------------------------------------------
        # Standard HTML Dashboard Response
        # --------------------------------------------------
        else:
            # Create LED status badge
            color_class = 'on-state' if led_state == 'ON' else 'off-state'
            state_badge = (
                '<span class="state {cls}">{st}</span>'
                .format(cls=color_class, st=led_state)
            )

            # Generate HTML page
            body = HTML.format(
                led_state=led_state,
                value=value
            )

            headers = (
                "HTTP/1.0 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                "Content-Length: {}\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).format(len(body))

        # Send response
        writer.write(headers.encode('utf-8'))
        writer.write(body.encode('utf-8'))
        await writer.drain()

    except Exception as e:
        print("Client error:", e)

    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass

# ==========================================================
# Connect to Wi-Fi
# ==========================================================
async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # If already connected
    if wlan.isconnected():
        print("Already connected.")
        print("🌐 IP Address :", wlan.ifconfig()[0])
        return wlan

    # Connect to Wi-Fi
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


# ==========================================================
# Main Program
# ==========================================================
async def main():
    # Connect to Wi-Fi
    wlan = await connect_wifi()

    # Start background tasks
    asyncio.create_task(task_blink())
    asyncio.create_task(task_background())

    # Start asynchronous web server
    await asyncio.start_server(handle_client, "0.0.0.0", 80)

    print("🌐 Async server listening on port 80")
    print("📱 Open your browser and visit:")
    print("   http://" + wlan.ifconfig()[0])

    # Keep the event loop alive forever
    while True:
        await asyncio.sleep(1)


# ==========================================================
# Program Entry Point
# ==========================================================
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n🛑 Program stopped by user.")
except Exception as e:
    print("\n❌ Error:", e)
finally:
    try:
        led_ctrl.off()
        led_blink.off()
    except:
        pass