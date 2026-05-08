from mfrc522 import MFRC522
from machine import Pin
import utime

# =========================
# LED SETUP (Onboard LED)
# =========================
led = Pin(25, Pin.OUT)

# =========================
# AUTHORIZED DATABASE
# =========================
# Example: store UID + name
AUTHORIZED_CARDS = [
    {"uid": [1, 192, 242, 6], "name": "Student A"},
    {"uid": [5, 186, 101, 6], "name": "Student B"},
]

# =========================
# RFID SETUP
# =========================
reader = MFRC522(
    sck=6,
    mosi=7,
    miso=4,
    rst=22,
    cs=5,
    spi_id=0
)

print("=== ACCESS CONTROL SYSTEM ===")
print("Scan your card...\n")


# =========================
# LED FUNCTIONS
# =========================
def access_granted():
    print("ACCESS GRANTED ✅")
    for _ in range(5):
        led.value(1)
        utime.sleep_ms(100)
        led.value(0)
        utime.sleep_ms(100)


def access_denied():
    print("ACCESS DENIED ❌")
    for _ in range(3):
        led.value(1)
        utime.sleep_ms(500)
        led.value(0)
        utime.sleep_ms(500)


# =========================
# CHECK AUTHORIZATION
# =========================
def is_authorized(uid):
    for card in AUTHORIZED_CARDS:
        if card["uid"] == uid:
            return True, card["name"]
    return False, None


# =========================
# MAIN LOOP
# =========================
while True:
    reader.init()

    (stat, tag_type) = reader.request(reader.REQIDL)

    if stat == reader.OK:
        print("\nCard detected!")

        (stat, uid) = reader.SelectTagSN()

        if stat == reader.OK:
            print("UID:", uid)

            authorized, name = is_authorized(uid)

            if authorized:
                print("Welcome,", name)
                access_granted()
            else:
                access_denied()

    utime.sleep_ms(500)