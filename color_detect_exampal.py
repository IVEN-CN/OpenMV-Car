# 单颜色RGB565斑点跟踪示例
#
# 该示例演示了使用OpenMV Cam进行单颜色RGB565跟踪。

import sensor
import time
import math

threshold_index = 0  # 0表示红色，1表示绿色，2表示蓝色

# 颜色跟踪阈值 (L最小值, L最大值, A最小值, A最大值, B最小值, B最大值)
# 下面的阈值用于跟踪一般的红色/绿色/蓝色物体。您可以根据需要进行调整...
thresholds = [
              (28, 52, -2, 71, -56, 68),  # red_thresholds
    (35, 71, -45, -7, -23, 50),  # green_thresholds
    (16, 61, 14, 59, -96, -33),  # blue_thresholds
]

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # 关闭自动增益以进行颜色跟踪
sensor.set_auto_whitebal(False)  # 关闭自动白平衡以进行颜色跟踪
clock = time.clock()

# 只有像素数大于"pixel_threshold"且面积大于"area_threshold"的斑点才会被"find_blobs"返回。
# 如果更改相机分辨率，请修改"pixels_threshold"和"area_threshold"的值。"merge=True"将合并图像中所有重叠的斑点。

while True:
    clock.tick()
    img = sensor.snapshot()
    img.lens_corr(1.8)
    for blob in img.find_blobs(
        [thresholds[threshold_index]],
        pixels_threshold=20000,
        area_threshold=20000,
        merge=True,
    ):
        # 这些值取决于斑点不是圆形的情况 - 否则它们将会抖动。
        if blob.elongation() > 0.5: # blob.elongation() = blob.w() / blob.h() 长宽比
            img.draw_edges(blob.min_corners(), color=(255, 0, 0))
            img.draw_line(blob.major_axis_line(), color=(0, 255, 0))
            img.draw_line(blob.minor_axis_line(), color=(0, 0, 255))
        # 这些值始终稳定。
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        # 注意 - 斑点的旋转角度只在0-180之间。
        img.draw_keypoints(
            [(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20
        )
    print(clock.fps())
