from mfrc522 import MFRC522
from machine import Pin
import utime

# =========================
# LED SETUP
# =========================
led = Pin(25, Pin.OUT)

# =========================
# DEFAULT KEY
# =========================
DEFAULT_KEY = [0xFF]*6

# =========================
# AUTHORIZED DATABASE
# UID + NAME (must match both)
# =========================
AUTHORIZED_CARDS = [
    {"uid": [12, 34, 56, 78], "name": "Somnang_2026"},
    {"uid": [111, 222, 333, 444], "name": "STUDENT_B"},
    {"uid": [1, 192, 242, 6], "name": "Student A"},
    {"uid": [5, 186, 101, 6], "name": "Student D"},
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

print("=== SECURE ACCESS CONTROL ===")
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
# READ TEXT FROM BLOCK
# =========================
def read_name_from_card(uid, block=1):
    if reader.auth(reader.AUTHENT1A, block, DEFAULT_KEY, uid) == reader.OK:
        (stat, data) = reader.read(block)
        reader.stop_crypto1()

        if stat == reader.OK:
            # Convert to string
            text = ''.join([chr(i) for i in data]).strip()
            return text
    return None

# =========================
# CHECK AUTHORIZATION
# =========================
def is_authorized(uid, name):
    for card in AUTHORIZED_CARDS:
        if card["uid"] == uid and card["name"] == name:
            return True
    return False

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

            # Read stored name
            name = read_name_from_card(uid)

            if name:
                print("Card Name:", name)

                if is_authorized(uid, name):
                    access_granted()
                else:
                    access_denied()
            else:
                print("Failed to read card data")
                access_denied()

    utime.sleep_ms(500)