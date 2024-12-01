import cv2
import time  # 导入时间模块以添加延迟

# 打开视频文件
cap = cv2.VideoCapture("D:\社团海报素材\QQ视频20241026110404.mp4")

# 获取视频的帧率和帧大小
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 定义视频编解码器并创建 VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_line_art_video.avi', fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 将图像转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 应用高斯模糊以减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 使用 Canny 边缘检测器
    edges = cv2.Canny(blurred, 50, 150)

    # 将结果写入视频文件
    out.write(edges)

    # 显示处理后的帧（可选）
    cv2.imshow('Line Art', edges)

    # 添加延迟，以保持与原视频帧率一致
    time.sleep(1 / fps)  # 根据原视频的帧率添加延迟

    # 如果按下 'q' 键，则退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源并关闭窗口
cap.release()
out.release()
cv2.destroyAllWindows()  # 如果显示了窗口，则取消注释此行