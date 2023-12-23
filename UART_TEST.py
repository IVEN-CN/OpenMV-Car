# Untitled - By: IVEN - Sun Dec 3 2023
import pyb
from pyb import UART
import time

ld1 = pyb.LED(1)
ld2 = pyb.LED(2)
ld3 = pyb.LED(3)

ser = UART(3,9600)

while True:
    ld1.on()
    s = ser.read(1)

    time.sleep_ms(250)
    ld1.off()
    time.sleep_ms(250)

    if s != None:
        ld2.on()
        print(s)
        time.sleep_ms(250)
        ld2.off()
        time.sleep_ms(250)
