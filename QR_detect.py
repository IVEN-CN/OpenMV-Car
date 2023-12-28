"""识别到二维码就闪红灯"""

import sensor
import time
import pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # 关闭自动增益
sensor.set_auto_whitebal(False)  # 关闭自动白平衡
ld1 = pyb.LED(1)

def QR_detect():

    sensor.set_pixformat(sensor.GRAYSCALE)  # 设置为灰度模式
    # 加强图像对比度，加强黑白边界
    sensor.set_contrast(3)
    while True:
        img = sensor.snapshot()
        img.lens_corr(1.8)
        for data in img.find_qrcodes():
            ld1.on()
            print(data.payload())
            print('')
            time.sleep(0.01)
            ld1.off()

QR_detect()
