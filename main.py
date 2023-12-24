import sensor
import time
from pyb import UART
import pyb

thresholds = [
    (53, 71, 51, 87, -12, 51),  # red_thresholds
    (35, 71, -45, -7, -23, 50),  # green_thresholds
    (16, 61, 14, 59, -96, -33),  # blue_thresholds
]

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # 设置图像格式为RGB565
sensor.set_framesize(sensor.QVGA)   # 设置图像大小为QVGA，
sensor.skip_frames(time=2000)   # 使新设置生效，跳过2000帧
sensor.set_auto_gain(False)  # 关闭自动增益
sensor.set_auto_whitebal(False)  # 关闭自动白平衡
ser = UART(3,9600)  # 初始化串口,波特率为9600,串口3,即P4,P5
ld1 = pyb.LED(1)
ld2 = pyb.LED(2)
ld3 = pyb.LED(3)

def detect_color(_index):
    """识别颜色"""
    ld1.on()
    ld2.on()
    ld3.on()
    while True:
        img = sensor.snapshot()
        for blob in img.find_blobs(
            [thresholds[_index]],   # 选择颜色,0为红色,1为绿色,2为蓝色
            pixels_threshold=5000,  # 识别到的颜色块像素阈值
            area_threshold=5000,
            merge=True              # 合并颜色块
        ):
            if blob.rect() != None:
                ld1.off()
                ld2.off()
                ld3.off()
                return ser.write(b'1')  # 发送信号给单片机,开始执行任务

def QR_detect():
    """识别二维码"""
    ld1.on()
    while True:
        img = sensor.snapshot()
        img.lens_corr(1.8)
        for data in img.find_qrcodes():
            ld1.off()
            return data.payload()

def color_choice(_sign):
    """选择颜色"""
    choices = {'11': 0, '22': 1, '33': 2}
    return choices.get(_sign[:2], 0)

def send_loop():
    while 1:
        time.sleep(0.2)
        ser.write(b'1')  # 发送信号给单片机,开始执行任务
        print(1)

message = QR_detect()    # 识别二维码,返回二维码信息
print(message)
detect_color(color_choice(message))    # 识别颜色


