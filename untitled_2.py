# Untitled - By: IVEN - Sat Dec 2 2023

import pyb, time

ld1 = pyb.LED(1)
ld2 = pyb.LED(2)
ld3 = pyb.LED(3)

while True:
    ld1.on()
    ld2.on()
    ld3.on()
    time.sleep(100)
    ld1.off()
    ld2.off()
    ld3.off()
