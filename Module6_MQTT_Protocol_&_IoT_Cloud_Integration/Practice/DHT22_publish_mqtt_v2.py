from machine import Pin
from time import sleep
import network
from umqtt.simple import MQTTClient
import config
import dht
import utime

# =========================================================
# GPIO SETUP
# =========================================================

# Onboard LED
led = Pin("LED", Pin.OUT)

# DHT22 Sensor
dht_sensor = dht.DHT22(Pin(15))

# =========================================================
# MQTT TOPICS
# =========================================================

MQTT_TOPIC_TEMPERATURE = b'pico/temperature'
MQTT_TOPIC_HUMIDITY = b'pico/humidity'

# Subscribe Topic
MQTT_TOPIC_LED = b'pico/led'

# =========================================================
# MQTT PARAMETERS
# =========================================================

MQTT_SERVER = config.mqtt_server
MQTT_PORT = 0

MQTT_USER = config.mqtt_username
MQTT_PASSWORD = config.mqtt_password

MQTT_CLIENT_ID = b"raspberrypi_picow"

MQTT_KEEPALIVE = 7200

MQTT_SSL = True
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

# =========================================================
# TERMINAL DECORATION
# =========================================================

def print_line():
    print("==================================================")

def print_header(title):
    print_line()
    print(title)
    print_line()

# =========================================================
# MQTT CALLBACK
# =========================================================

def mqtt_callback(topic, msg):

    print_header("MQTT SUBSCRIBE MESSAGE")

    print("Topic   :", topic.decode())
    print("Message :", msg.decode())

    # LED Control
    if topic == MQTT_TOPIC_LED:

        if msg == b'ON':
            led.on()
            print("LED STATUS : ON")

        elif msg == b'OFF':
            led.off()
            print("LED STATUS : OFF")

    print_line()

# =========================================================
# DHT22 SENSOR
# =========================================================

def get_sensor_readings():

    try:

        dht_sensor.measure()

        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        return temperature, humidity

    except Exception as e:

        print_header("DHT22 SENSOR ERROR")
        print("Error :", e)

        return None, None

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

    timeout = 15

    while timeout > 0:

        status = wlan.status()

        if status >= 3:
            break

        timeout -= 1

        print("Waiting for connection...")

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

        # Callback Function
        client.set_callback(mqtt_callback)

        # Connect MQTT
        client.connect()

        print("MQTT Broker Connected")

        # Subscribe Topic
        client.subscribe(MQTT_TOPIC_LED)

        print("Subscribed Topic :", MQTT_TOPIC_LED.decode())

        print_line()

        return client

    except Exception as e:

        print_header("MQTT CONNECTION ERROR")
        print("Error :", e)

        raise

# =========================================================
# MQTT PUBLISH
# =========================================================

def publish_mqtt(topic, value):

    try:

        client.publish(topic, str(value))

        print_header("MQTT PUBLISH")

        print("Topic     :", topic.decode())
        print("Value     :", value)

        print("Published : SUCCESS")

        print_line()

    except Exception as e:

        print("Publish Error :", e)

# =========================================================
# MAIN PROGRAM
# =========================================================

try:

    print("\n")
    print("Raspberry Pi Pico W MQTT Monitor")
    print("Starting System...")
    print("\n")

    # Connect WiFi
    if not initialize_wifi(
        config.wifi_ssid,
        config.wifi_password
    ):

        print("Program Stopped")

    else:

        # Connect MQTT
        client = connect_mqtt()

        while True:

            # Check Subscribe Messages
            client.check_msg()

            # Get DHT22 Readings
            temperature, humidity = get_sensor_readings()

            if temperature is not None:

                # Publish Temperature
                publish_mqtt(
                    MQTT_TOPIC_TEMPERATURE,
                    temperature
                )

                # Publish Humidity
                publish_mqtt(
                    MQTT_TOPIC_HUMIDITY,
                    humidity
                )

                # Terminal Dashboard
                print_header("LIVE SENSOR DASHBOARD")

                print("Time        :", utime.localtime())
                print("Temperature :", temperature, "°C")
                print("Humidity    :", humidity, "%")

                print_line()

            # Blink LED
            led.toggle()

            # Delay
            sleep(10)

except Exception as e:

    print_header("SYSTEM ERROR")
    print("Error :", e)