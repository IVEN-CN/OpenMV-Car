import sensor
import time
from pyb import UART
import pyb

thresholds = [
    (35, 76, 12, 81, 8, 127),  # red_thresholds
    (35, 71, -45, -7, -23, 50),  # green_thresholds
    (16, 61, 14, 59, -96, -33),  # blue_thresholds
]

ser = UART(3,9600)  # 初始化串口,波特率为9600,串口3,即P4,P5
ld1 = pyb.LED(1)
ld2 = pyb.LED(2)
ld3 = pyb.LED(3)

def detect_color(_index):
    """识别颜色"""
    ld1.on()
    ld2.on()
    ld3.on()
    sensor.reset()
    sensor.set_framesize(sensor.QVGA)   # 设置图像大小为QVGA，
    sensor.set_pixformat(sensor.RGB565)  # 设置图像格式为RGB565
    sensor.skip_frames(time=2000)   # 使新设置生效，跳过2000帧
    sensor.set_auto_gain(False)  # 关闭自动增益
    sensor.set_auto_whitebal(False)  # 关闭自动白平衡
    while True:
        img = sensor.snapshot()
        img.lens_corr(1.8)
        for blob in img.find_blobs(
            [thresholds[_index]],   # 选择颜色,0为红色,1为绿色,2为蓝色
            pixels_threshold=20000,  # 识别到的颜色块像素阈值
            area_threshold=20000,
            merge=True              # 合并颜色块
        ):
            if blob.rect() != None:
                ld1.off()
                ld2.off()
                ld3.off()
                return send_loop(1)  # 发送信号给单片机,开始执行任务

def QR_detect():
    """识别二维码"""
    ld1.on()
    sensor.reset()
    sensor.set_framesize(sensor.QVGA)   # 设置图像大小为QVGA，
    sensor.set_pixformat(sensor.GRAYSCALE)  # 设置为灰度模式
    # 加强图像对比度，加强黑白边界
    sensor.set_contrast(500)
    sensor.skip_frames(time=2000)   # 使新设置生效，跳过2000帧
    sensor.set_auto_gain(False)  # 关闭自动增益
    sensor.set_auto_whitebal(False)  # 关闭自动白平衡
    while True:
        img = sensor.snapshot()
        img.lens_corr(1.8)
        for data in img.find_qrcodes():
            ld1.off()
            return data.payload(),send_loop(2)

def color_choice(_sign):
    """选择颜色"""
    choices = {'11': 0, '22': 1, '33': 2}
    return choices.get(_sign[:2], 0)

def send_loop(sign):
    dict = {1:b'1',2:b'2'}
    mes = dict.get(sign,None)
    for i in range(3):
        time.sleep(0.01)
        ser.write(mes)  # 发送信号给单片机,开始执行任务

message, _ = QR_detect()    # 识别二维码,返回二维码信息
print(message)
detect_color(color_choice(message))    # 识别颜色


