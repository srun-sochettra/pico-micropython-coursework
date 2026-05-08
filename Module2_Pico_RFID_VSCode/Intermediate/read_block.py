# read_block.py
# Authenticate and read 16 bytes from Block 1, Sector 0

from mfrc522 import MFRC522

reader = MFRC522(
    sck=6,
    mosi=7,
    miso=4,
    rst=22,
    cs=5,
    spi_id=0
)
KEY    = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
BLOCK  = 1   # Sector 0, Block 1 (safe user block)

print('Waiting for card...')

while True:
    stat, tag_type = reader.request(reader.REQIDL)
    if stat == reader.OK:
        stat, uid = reader.anticoll()
        if stat == reader.OK:
            reader.select_tag(uid)
            stat = reader.auth(reader.AUTHENT1A, BLOCK, KEY, uid)
            if stat == reader.OK:
                data = reader.read(BLOCK)
                print(f'Block {BLOCK} data (raw bytes): {data}')
                text = bytes(data).decode('utf-8', errors='replace').rstrip('\x00')
                print(f'As text: "{text}"')
            else:
                print('Authentication failed!')
            reader.stop_crypto1()  # ALWAYS call this after auth
            break
