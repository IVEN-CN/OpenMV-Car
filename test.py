import sensor
import time
import math
from pyb import UART
import pyb

thresholds = [
    (21, 72, 15, 81, -21, 51),  # generic_red_thresholds
    (0, 100, -128, 125, -88, -24),  # generic_green_thresholds
    (6, 22, 3, 19, -49, -28),
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
        ld1.on()
        ld2.on()
        ld3.on()
        clock.tick()
        img = sensor.snapshot()
        for blob in img.find_blobs(
            [thresholds[_index]],
            pixels_threshold=2000,
            area_threshold=2000,
            merge=True
        ):
            # These values depend on the blob not being circular - otherwise they will be shaky.

            img.draw_rectangle(blob.rect())
#             绘制中心十字
            img.draw_cross(blob.cx(), blob.cy())
#             绘制中心圈
            img.draw_keypoints(
                [(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20
            )

#            print(blob.rect())
            if blob.rect() != None:
                ld1.off()
#                ld2.off()
                ld3.off()
                return 1
#                print(1)



def QR_detect():
    while True:
        ld1.on()
        ld2.on()
        ld3.on()


        img = sensor.snapshot()
        img.lens_corr(1.8)
        for data in img.find_qrcodes():
            return data.payload(),1
        time.sleep_ms(25)
        ld1.off()
        ld2.off()
        ld3.off()
        time.sleep_ms(25)

def color_choice(_sign):
    if _sign == '11':
        return 0
    elif _sign == '22':
        return 1
    elif _sign == '33':
        return 2

info, sign = QR_detect()
print(info)
index = color_choice(info)
#while (detect_color(index) == 1):
#    ld2.on()
print(detect_color(index))
