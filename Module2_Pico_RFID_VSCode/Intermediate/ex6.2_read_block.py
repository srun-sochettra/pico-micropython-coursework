# read_block.py
# Authenticate and read 16 bytes from Block 1, Sector 0

from mfrc522 import MFRC522
import utime

# Default key (Factory key for most RFID cards)
DEFAULT_KEY = [0xFF]*6

# Initialize RFID
reader = MFRC522(
    sck=6,
    mosi=7,
    miso=4,
    rst=22,
    cs=5,
    spi_id=0
)

print("=== RFID READ BLOCK ===")
print("Place card near reader...\n")

while True:
    reader.init()

    # Step 1: Request card
    (stat, tag_type) = reader.request(reader.REQIDL)

    if stat == reader.OK:
        print("Card detected!")

        # Step 2: Get UID
        (stat, uid) = reader.SelectTagSN()

        if stat == reader.OK:
            print("UID:", uid)

            # Step 3: Authenticate block
            block_addr = 1  # Block 1 (Sector 0)

            if reader.auth(reader.AUTHENT1A, block_addr, DEFAULT_KEY, uid) == reader.OK:
                print("Authentication success")

                # Step 4: Read block
                (stat, data) = reader.read(block_addr)

                if stat == reader.OK:
                    print("Raw Data:", data)

                    # Convert to string
                    text = ''.join([chr(i) if 32 <= i <= 126 else '.' for i in data])
                    print("Text:", text)

                else:
                    print("Read failed")

                reader.stop_crypto1()

            else:
                print("Authentication error")

    utime.sleep_ms(500)