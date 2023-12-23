# Single Color RGB565 Blob Tracking Example
#
# This example shows off single color RGB565 tracking using the OpenMV Cam.
# 识别到二维码就闪绿灯

import sensor
import time
import math
from pyb import UART
import pyb

thresholds = [
    (53, 76, 27, 105, 3, 127),  # generic_red_thresholds
    (0, 100, -128, 125, -88, -24),  # generic_green_thresholds
    (0, 100, -128, 125, -59, -32),
]  # generic_blue_thresholds

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # 关闭自动增益
sensor.set_auto_whitebal(False)  # 关闭自动白平衡
ser = UART(3,19200)
clock = time.clock()
ld1 = pyb.LED(1)
ld2 = pyb.LED(2)
ld3 = pyb.LED(3)

def QR_detect():
    while True:
        img = sensor.snapshot()
        img.lens_corr(1.8)
        for data in img.find_qrcodes():
            ld1.on()
            print (data.payload())
            time.sleep(0.01)
            ld1.off()
            time.sleep(0.01)

QR_detect()
