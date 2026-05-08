# blinking.py
# Blink the onboard LED every 0.5 seconds
# Works on both Pico and Pico W

from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)   # 'LED' works on both Pico and Pico W
                            # Use Pin(25, Pin.OUT) if you only have original Pico
print('Blinking LED — press Stop to end')

while True:
    led.value(not led.value())   # toggle: 1 becomes 0, 0 becomes 1
    sleep(0.5)                   # wait 500 milliseconds
