import network
import socket
from machine import Pin
from time import sleep

# ============================================
# LED Configuration
# ============================================

led = Pin("LED", Pin.OUT)

# ============================================
# Access Point Configuration
# ============================================

SSID = '14_Srun_Sochettra'
PASSWORD = '12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)

# Configure AP
ap.config(
    essid=SSID,
    password=PASSWORD
)

print("\n===================================")
print("   Pico W Access Point Started")
print("===================================")

# Wait for AP startup
sleep(2)

# Display network information
ip = ap.ifconfig()[0]

print("SSID      :", SSID)
print("Password  :", PASSWORD)
print("IP Address:", ip)

# ============================================
# HTML Webpage
# ============================================

def webpage():
    
    led_state = "OFF"
    
    if led.value() == 1:
        led_state = "ON"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pico W IoT Control</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>
            body {{
                font-family: Arial;
                text-align: center;
                background-color: #f2f2f2;
                margin-top: 50px;
            }}

            h1 {{
                color: #333;
            }}

            .card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                width: 300px;
                margin: auto;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
            }}

            .button {{
                display: inline-block;
                padding: 15px 25px;
                font-size: 18px;
                margin: 10px;
                cursor: pointer;
                border: none;
                border-radius: 5px;
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

            <h1>Pico W IoT Server</h1>

            <h2>LED Status: {led_state}</h2>

            <a href="/led/on">
                <button class="button on">LED ON</button>
            </a>

            <a href="/led/off">
                <button class="button off">LED OFF</button>
            </a>

        </div>

    </body>
    </html>
    """

    return html

# ============================================
# Socket Web Server
# ============================================

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

server = socket.socket()
server.bind(addr)
server.listen(1)

print("\nWeb Server Running...")
print("Open browser and visit:")
print("http://" + ip)

# ============================================
# Main Server Loop
# ============================================

while True:

    try:
        client, addr = server.accept()

        print('\nClient connected from', addr)

        request = client.recv(1024)

        request = str(request)

        print("Request:")
        print(request)

        # ====================================
        # LED Control
        # ====================================

        if '/led/on' in request:
            print("LED ON")
            led.value(1)

        if '/led/off' in request:
            print("LED OFF")
            led.value(0)

        # ====================================
        # Send Response
        # ====================================

        response = webpage()

        client.send('HTTP/1.1 200 OK\r\n')
        client.send('Content-Type: text/html\r\n')
        client.send('Connection: close\r\n\r\n')

        client.sendall(response)

        client.close()

    except Exception as e:
        print("Error:", e)