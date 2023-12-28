"""单颜色RGB565斑点跟踪示例
该示例演示了使用OpenMV Cam进行单颜色RGB565跟踪。
用于调整颜色阈值
"""
import sensor
import time
import math

threshold_index =  2 # 0表示红色，1表示绿色，2表示蓝色

# 颜色跟踪阈值 (L最小值, L最大值, A最小值, A最大值, B最小值, B最大值)
# 下面的阈值用于跟踪一般的红色/绿色/蓝色物体。您可以根据需要进行调整...
thresholds = [
    (5, 73, 2, 92, -21, 45),  # red_thresholds
    (19, 94, -63, -17, -23, 45),  # green_thresholds
    (15, 59, -17, 37, -72, -16),  # blue_thresholds
]

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # 关闭自动增益以进行颜色跟踪
sensor.set_auto_whitebal(False)  # 关闭自动白平衡以进行颜色跟踪
clock = time.clock()

# 只有像素数大于"pixel_threshold"且面积大于"area_threshold"的颜色区域才会被"find_blobs"返回。
# 如果更改相机分辨率，请修改"pixels_threshold"和"area_threshold"的值。"merge=True"将合并图像中所有重叠的颜色区域。

while True:
    clock.tick()
    img = sensor.snapshot()
    img.lens_corr(1.8)
    for blob in img.find_blobs(
        [thresholds[threshold_index]],
        pixels_threshold=20000,
        area_threshold=20000,
        merge=False,
    ):
        # 这些值取决于颜色区域不是圆形的情况 - 否则它们将会抖动。
        if blob.elongation() > 0.5: # blob.elongation() = blob.w() / blob.h() 长宽比
            img.draw_edges(blob.min_corners(), color=(255, 0, 0))       # 画出颜色区域的最小外接矩形
            img.draw_line(blob.major_axis_line(), color=(0, 255, 0))    # 画出颜色区域的主轴
            img.draw_line(blob.minor_axis_line(), color=(0, 0, 255))    # 画出颜色区域的次轴
        # 这些值始终稳定。
        img.draw_rectangle(blob.rect())                                 # 画出颜色区域的最小外接矩形
        img.draw_cross(blob.cx(), blob.cy())                            # 画出颜色区域的中心点
        img.draw_keypoints(
            [(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20
        )                                                               # 画出颜色区域的中心点和旋转角度
    print(clock.fps())
