# 单色灰度斑点跟踪示例
#
# 该示例演示了使用OpenMV Cam进行单色灰度跟踪。

import sensor
import time
import math

# 颜色跟踪阈值（灰度最小值，灰度最大值）
# 下面的灰度阈值设置为仅查找非常明亮的白色区域。
thresholds = (245, 255)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.VGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # 必须关闭自动增益以进行颜色跟踪
sensor.set_auto_whitebal(False)  # 必须关闭自动白平衡以进行颜色跟踪
clock = time.clock()

# 仅返回像素数大于“pixel_threshold”和面积大于“area_threshold”的斑点
# “find_blobs”函数。如果更改相机分辨率，请更改“pixels_threshold”和“area_threshold”。
# “merge=True”将图像中所有重叠的斑点合并。

while True:
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs(
        [thresholds], pixels_threshold=100, area_threshold=100, merge=True
    ):
        # 这些值取决于斑点不是圆形-否则它们将会抖动。
        if blob.elongation() > 0.5:
            img.draw_edges(blob.min_corners(), color=0)
            img.draw_line(blob.major_axis_line(), color=0)
            img.draw_line(blob.minor_axis_line(), color=0)
        # 这些值始终稳定。
        img.draw_rectangle(blob.rect(), color=127)
        img.draw_cross(blob.cx(), blob.cy(), color=127)
        # 注意-斑点旋转仅在0-180之间唯一。
        img.draw_keypoints(
            [(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))],
            size=40,
            color=127,
        )
    print(clock.fps())
