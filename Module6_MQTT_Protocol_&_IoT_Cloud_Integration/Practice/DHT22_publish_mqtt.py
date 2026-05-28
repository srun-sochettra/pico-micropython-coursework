from machine import Pin
from time import sleep
import network
from umqtt.simple import MQTTClient
import config
import dht

# MQTT Topics
MQTT_TOPIC_TEMPERATURE = 'pico/temperature'
MQTT_TOPIC_HUMIDITY = 'pico/humidity'

# MQTT Parameters
MQTT_SERVER = config.mqtt_server
MQTT_PORT = 0
MQTT_USER = config.mqtt_username
MQTT_PASSWORD = config.mqtt_password

MQTT_CLIENT_ID = b"raspberrypi_picow"
MQTT_KEEPALIVE = 7200

MQTT_SSL = True
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

# Initialize DHT22
dht_sensor = dht.DHT22(Pin(15))


def get_sensor_readings():
    try:
        dht_sensor.measure()

        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        return temperature, humidity

    except Exception as e:
        print("DHT22 Error:", e)
        return None, None


def initialize_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(ssid, password)

    timeout = 10

    while timeout > 0:
        if wlan.status() >= 3:
            break

        timeout -= 1
        print("Waiting for WiFi...")
        sleep(1)

    if wlan.status() != 3:
        return False

    print("WiFi Connected")
    print("IP Address:", wlan.ifconfig()[0])

    return True


def connect_mqtt():
    try:
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

        print("MQTT Connected")

        return client

    except Exception as e:
        print("MQTT Connection Error:", e)
        raise


def publish_mqtt(topic, value):
    client.publish(topic, str(value))
    print("Topic:", topic)
    print("Value:", value)
    print("Published Successfully")


try:

    if not initialize_wifi(
        config.wifi_ssid,
        config.wifi_password
    ):
        print("WiFi Connection Failed")

    else:

        client = connect_mqtt()

        while True:

            temperature, humidity = get_sensor_readings()

            if temperature is not None:

                publish_mqtt(
                    MQTT_TOPIC_TEMPERATURE,
                    temperature
                )

                publish_mqtt(
                    MQTT_TOPIC_HUMIDITY,
                    humidity
                )

            sleep(10)

except Exception as e:
    print("Error:", e)