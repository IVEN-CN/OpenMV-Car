import sensor
import time
from pyb import UART
import pyb

thresholds = [
    (53, 76, 27, 105, 3, 127),  # red_thresholds
    (0, 100, -128, 125, -88, -24),  # green_thresholds
    (0, 100, -128, 125, -59, -32),  # blue_thresholds
]  

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # 设置图像格式为RGB565
sensor.set_framesize(sensor.QVGA)   # 设置图像大小为QVGA，
sensor.skip_frames(time=2000)   # 使新设置生效，跳过2000帧
sensor.set_auto_gain(False)  # 关闭自动增益
sensor.set_auto_whitebal(False)  # 关闭自动白平衡
ser = UART(3,9600)  # 初始化串口,波特率为9600,串口3,即P4,P5
ld1 = pyb.LED(1)
ld3 = pyb.LED(3)

def detect_color(_index):
    """识别颜色"""
    while True:
        img = sensor.snapshot()
        for blob in img.find_blobs(
            [thresholds[_index]],   # 选择颜色,0为红色,1为绿色,2为蓝色
            pixels_threshold=2000,  # 识别到的颜色块像素阈值
            merge=True              # 合并颜色块
        ):
            ld1.on()
            ld3.on()
            if blob.rect() != None:
                ld1.off()
                ld3.off()
                return 1

def QR_detect():
    """识别二维码"""
    while True:
        img = sensor.snapshot()
        img.lens_corr(1.8)
        for data in img.find_qrcodes():
            return data.payload()

def color_choice(_sign):
    """选择颜色"""
    choices = {'11': 0, '22': 1, '33': 2}
    return choices.get(_sign[:2], 0)

message = QR_detect()    # 识别二维码,返回二维码信息
print(message)
detect_color(color_choice(message))    # 识别颜色
ser.write('1')  # 发送信号给单片机,开始执行任务

