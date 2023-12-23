# Single Color RGB565 Blob Tracking Example
#
# This example shows off single color RGB565 tracking using the OpenMV Cam.

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

def detect_color(_index):
    while True:
        clock.tick()
        img = sensor.snapshot()
        for blob in img.find_blobs(
            [thresholds[_index]],
            pixels_threshold=2000,
            merge=True
        ):
            # These values depend on the blob not being circular - otherwise they will be shaky.

            # img.draw_rectangle(blob.rect())
            # 绘制中心十字
            # img.draw_cross(blob.cx(), blob.cy())
            # 绘制中心圈
            # img.draw_keypoints(
            #     [(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20
            # )
#            print(blob.rect())
            if blob.rect() != None:
                ld1.off()
#                ld2.off()
                ld3.off()
                return 1
#                print(1)

def QR_detect():
    while True:
        img = sensor.snapshot()
        img.lens_corr(1.8)
        for data in img.find_qrcodes():
            return data.payload()

def color_choice(_sign):
    choices = {'11': 0, '22': 1, '33': 2}
    return choices.get(_sign[:2], 0)

def send(v):
    ser.write('s')
    ser.write(v)
    ser.write('e')

message = QR_detect()    # 识别二维码,返回二维码信息
detect_color(color_choice(message))    # 识别颜色
ser.write('1')

