# ==========================================================
# Raspberry Pi Pico 2W Socket Web Server Example
# Section 2.5: Sockets
# ==========================================================
# This program demonstrates:
#   1. Connecting Pico 2W to Wi-Fi
#   2. Creating a TCP socket
#   3. Binding to port 80
#   4. Listening for HTTP requests
#   5. Parsing URLs
#   6. Controlling the onboard LED
#   7. Sending HTML responses
# ==========================================================

import network
import socket
import time
from machine import Pin

# ==========================================================
# Wi-Fi Credentials
# ==========================================================
from secrets import SSID, PASSWORD
# ==========================================================
# Hardware Setup
# ==========================================================
# Pico W / Pico 2W onboard LED
led = Pin("LED", Pin.OUT)
led.off()

# Track LED state as text
led_state = "OFF"

# ==========================================================
# HTML Web Page Template
# ==========================================================
HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Pico 2W Socket Server</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 30px;
            background: #f4f7fb;
        }}
        h1 {{
            color: #006480;
        }}
        h2 {{
            color: #E05A00;
        }}
        .card {{
            max-width: 500px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        button {{
            padding: 14px 28px;
            font-size: 18px;
            margin: 8px;
            border: none;
            border-radius: 8px;
            color: white;
            cursor: pointer;
        }}
        .on {{
            background: #4CAF50;
        }}
        .off {{
            background: #F44336;
        }}
        .state {{
            font-size: 24px;
            font-weight: bold;
            color: {color};
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Raspberry Pi Pico 2W</h1>
        <h2>Socket Web Server</h2>

        <a href="/lighton">
            <button class="on">Turn ON</button>
        </a>

        <a href="/lightoff">
            <button class="off">Turn OFF</button>
        </a>

        <p>LED State:</p>
        <p class="state">{state}</p>

        <p>IP Address: <strong>{ip}</strong></p>
    </div>
</body>
</html>
"""

# ==========================================================
# Connect to Wi-Fi
# ==========================================================
def connect_wifi():
    print("\n========================================")
    print("Connecting to Wi-Fi")
    print("========================================")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Disconnect if already connected
    if wlan.isconnected():
        wlan.disconnect()
        time.sleep(1)

    print("SSID:", SSID)
    print("Connecting", end="")

    wlan.connect(SSID, PASSWORD)

    timeout = 20  # seconds
    while not wlan.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(1)
        timeout -= 1

    print()

    if wlan.isconnected():
        print("Wi-Fi Connected Successfully!")
        print("IP Address :", wlan.ifconfig()[0])
        print("Subnet Mask:", wlan.ifconfig()[1])
        print("Gateway    :", wlan.ifconfig()[2])
        print("DNS Server :", wlan.ifconfig()[3])
        return wlan
    else:
        raise RuntimeError("Failed to connect to Wi-Fi")


# ==========================================================
# Generate Web Page
# ==========================================================
def generate_html(ip_address):
    global led_state

    # Select color based on LED state
    if led_state == "ON":
        color = "#4CAF50"
    else:
        color = "#F44336"

    # Replace placeholders
    return HTML.format(
        state=led_state,
        color=color,
        ip=ip_address
    )


# ==========================================================
# Parse HTTP Request
# ==========================================================
def process_request(request):
    global led_state

    # Convert bytes to string if needed
    if isinstance(request, bytes):
        request = request.decode("utf-8")

    # Print only the first line
    first_line = request.split("\r\n")[0]
    print("HTTP Request:", first_line)

    # URL routing
    if "GET /lighton" in request:
        led.on()
        led_state = "ON"
        print("Action: LED ON")

    elif "GET /lightoff" in request:
        led.off()
        led_state = "OFF"
        print("Action: LED OFF")


# ==========================================================
# Create HTTP Response
# ==========================================================
def create_response(body):
    headers = (
        "HTTP/1.0 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "Content-Length: {}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).format(len(body))

    return headers + body


# ==========================================================
# Start Socket Server
# ==========================================================
def start_server(ip_address):
    print("\n========================================")
    print("Starting Socket Server")
    print("========================================")

    # Resolve address
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    print("Bind Address:", addr)

    # Create TCP socket
    s = socket.socket()

    # Allow quick restart
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to IP/Port
    s.bind(addr)

    # Listen for connections
    s.listen(5)

    print("Server is listening on port 80")
    print("Open your browser and visit:")
    print("http://" + ip_address)
    print()

    # Main server loop
    while True:
        try:
            print("Waiting for client connection...")

            # Accept client connection
            conn, client_addr = s.accept()
            print("Client Connected:", client_addr)

            # Receive HTTP request
            request = conn.recv(1024)

            # Process URL
            process_request(request)

            # Generate HTML page
            body = generate_html(ip_address)

            # Build HTTP response
            response = create_response(body)

            # Send response
            conn.send(response)

            # Close connection
            conn.close()

            print("Response sent. Connection closed.\n")

        except KeyboardInterrupt:
            print("\nServer stopped by user.")
            s.close()
            break

        except Exception as e:
            print("Error:", e)
            try:
                conn.close()
            except:
                pass


# ==========================================================
# Main Program
# ==========================================================
def main():
    wlan = connect_wifi()
    ip = wlan.ifconfig()[0]
    start_server(ip)


# Run the program
main()