from machine import Pin
from time import sleep
import network
from umqtt.simple import MQTTClient
import config
import utime

# =========================================================
# GPIO SETUP
# =========================================================

# Built-in LED
led = Pin("LED", Pin.OUT)

# =========================================================
# MQTT TOPICS
# =========================================================

MQTT_TOPIC_LED = b'pico/led'

# =========================================================
# MQTT PARAMETERS
# =========================================================

MQTT_SERVER = config.mqtt_server
MQTT_PORT = 0

MQTT_USER = config.mqtt_username
MQTT_PASSWORD = config.mqtt_password

MQTT_CLIENT_ID = b'raspberrypi_picow'

MQTT_KEEPALIVE = 7200

MQTT_SSL = True
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

# =========================================================
# TERMINAL DESIGN
# =========================================================

def print_line():
    print("==================================================")

def print_header(title):
    print_line()
    print(title)
    print_line()

# =========================================================
# WIFI CONNECTION
# =========================================================

def initialize_wifi(ssid, password):

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print_header("WIFI CONNECTION")

    print("Connecting to WiFi...")
    print("SSID :", ssid)

    wlan.connect(ssid, password)

    timeout = 20

    while timeout > 0:

        if wlan.status() >= 3:
            break

        timeout -= 1

        print("Waiting for WiFi connection...")

        led.toggle()

        sleep(1)

    if wlan.status() != 3:

        print("WiFi Connection Failed")
        print_line()

        return False

    else:

        led.on()

        print("WiFi Connected Successfully")
        print("IP Address :", wlan.ifconfig()[0])
        print("Subnet Mask:", wlan.ifconfig()[1])
        print("Gateway    :", wlan.ifconfig()[2])
        print("DNS        :", wlan.ifconfig()[3])

        print_line()

        return True

# =========================================================
# MQTT CONNECTION
# =========================================================

def connect_mqtt():

    try:

        print_header("MQTT CONNECTION")

        print("Connecting to MQTT Broker...")
        print("Server :", MQTT_SERVER.decode())

        client = MQTTClient(
            client_id=MQTT_CLIENT_ID,
            server=MQTT_SERVER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            keepalive=MQTT_KEEPALIVE,
            ssl=MQTT_SSL,
            ssl_params=MQTT_SSL_PARAMS
        )

        client.connect()

        print("MQTT Broker Connected Successfully")

        print_line()

        return client

    except Exception as e:

        print_header("MQTT CONNECTION ERROR")

        print("Error :", e)

        print_line()

        return None

# =========================================================
# MQTT SUBSCRIBE
# =========================================================

def subscribe(client, topic):

    client.subscribe(topic)

    print_header("MQTT SUBSCRIPTION")

    print("Subscribed Topic :", topic.decode())
    print("Subscription     : SUCCESS")

    print_line()

# =========================================================
# MQTT CALLBACK FUNCTION
# =========================================================

def my_callback(topic, message):

    print_header("MQTT MESSAGE RECEIVED")

    print("Topic   :", topic.decode())
    print("Message :", message.decode())

    # LED Control
    if message == b'ON':

        led.on()

        print("LED STATUS : ON")

    elif message == b'OFF':

        led.off()

        print("LED STATUS : OFF")

    else:

        print("Unknown Command")

    print_line()

# =========================================================
# MAIN PROGRAM
# =========================================================

try:

    print("\n")
    print("Raspberry Pi Pico W MQTT LED Controller")
    print("System Starting...")
    print("\n")

    # WiFi Connection
    if not initialize_wifi(
        config.wifi_ssid,
        config.wifi_password
    ):

        print("Program Stopped")

    else:

        # MQTT Connection
        client = connect_mqtt()

        if client is not None:

            # Set Callback
            client.set_callback(my_callback)

            # Subscribe Topic
            subscribe(client, MQTT_TOPIC_LED)

            # Main Loop
            while True:

                # Check Incoming MQTT Messages
                client.check_msg()

                # Heartbeat Monitor
                print_header("SYSTEM RUNNING")

                print("Time :", utime.localtime())
                print("Listening Topic :", MQTT_TOPIC_LED.decode())
                print("MQTT Status : CONNECTED")
                print("WiFi Status : CONNECTED")

                print_line()

                sleep(5)

except Exception as e:

    print_header("SYSTEM ERROR")

    print("Error :", e)

    print_line()