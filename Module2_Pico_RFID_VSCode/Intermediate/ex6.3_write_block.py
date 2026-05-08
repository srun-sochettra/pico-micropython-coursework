# write_block.py
# Write a 16-byte string to Block 1, Sector 0

from mfrc522 import MFRC522
import utime

DEFAULT_KEY = [0xFF]*6

reader = MFRC522(
    sck=6,
    mosi=7,
    miso=4,
    rst=22,
    cs=5,
    spi_id=0
)

print("=== RFID WRITE BLOCK ===")
print("Place card near reader...\n")

# Data to write (must be EXACTLY 16 bytes)
text = "Student B"
data = [ord(c) for c in text]

# Pad to 16 bytes
while len(data) < 16:
    data.append(32)  # space

while True:
    reader.init()

    (stat, tag_type) = reader.request(reader.REQIDL)

    if stat == reader.OK:
        print("Card detected!")

        (stat, uid) = reader.SelectTagSN()

        if stat == reader.OK:
            print("UID:", uid)

            block_addr = 1

            if reader.auth(reader.AUTHENT1A, block_addr, DEFAULT_KEY, uid) == reader.OK:
                print("Authentication success")

                # Write data
                if reader.write(block_addr, data) == reader.OK:
                    print("Write successful!")

                    # Verify by reading
                    (stat, new_data) = reader.read(block_addr)
                    if stat == reader.OK:
                        print("Verify:", new_data)

                else:
                    print("Write failed")

                reader.stop_crypto1()

            else:
                print("Authentication error")

    utime.sleep_ms(1000)