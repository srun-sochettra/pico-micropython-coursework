# temperature.py
# Read the RP2040 internal temperature sensor

from machine import ADC
import time

sensor = ADC(4)           # ADC channel 4 = internal temperature sensor
VOLT_REF = 3.3            # Pico reference voltage
CONVERSION = 65535        # 16-bit ADC max

while True:
    raw   = sensor.read_u16()                    # 0 – 65535
    volts = raw * (VOLT_REF / CONVERSION)        # convert to volts
    temp  = 27 - (volts - 0.706) / 0.001721     # RP2040 formula
    print(f"Temperature: {temp:.1f} °C  |  ADC raw: {raw}")
    time.sleep(1)
