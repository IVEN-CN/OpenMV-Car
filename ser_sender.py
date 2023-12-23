# Untitled - By: IVEN - Sun Dec 3 2023
import pyb
from pyb import UART
import time
import sensor

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # 关闭自动增益
sensor.set_auto_whitebal(False)  # 关闭自动白平衡

ld1 = pyb.LED(1)
ld2 = pyb.LED(2)
ld3 = pyb.LED(3)

ser = UART(3,9600)

def QR_detect():
    while True:
        img = sensor.snapshot()
        img.lens_corr(1.8)
        for data in img.find_qrcodes():
            ld2.on()
            time.sleep_ms(50)
            ld2.off()
            time.sleep_ms(50)
            return data.payload(),1

info, sign = QR_detect()
if sign:
    ser.write(info)
    print(info)
