import cv2
import time
import os
import pickle
from blessed import Terminal

# 初始化 blessed 的终端对象
term = Terminal()

# 更复杂的字符集，用于增强灰度映射效果
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "


# 将每个像素映射为ASCII字符
def pixel_to_ascii(pixel_value):
    ascii_index = pixel_value * len(ASCII_CHARS) // 256
    return ASCII_CHARS[min(ascii_index, len(ASCII_CHARS) - 1)]


# 将图像转换为ASCII艺术字符，并保留颜色信息
def image_to_ascii_colored(frame, width=120):
    height, orig_width, _ = frame.shape
    aspect_ratio = height / orig_width
    new_width = width
    new_height = int(aspect_ratio * new_width * 0.43)
    resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    # 使用列表存储所有行
    ascii_image = []
    for y in range(new_height):
        line = []
        last_color = None
        for x in range(new_width):
            gray = gray_frame[y, x]
            ascii_char = pixel_to_ascii(gray)
            b, g, r = resized_frame[y, x]

            current_color = (r, g, b)
            if current_color != last_color:
                line.append(term.color_rgb(r, g, b))
                last_color = current_color
            line.append(ascii_char)
        line.append(term.normal)  # 重置颜色
        ascii_image.append(''.join(line))
    return "\n".join(ascii_image)


# 将视频的每一帧预计算并缓存到本地
def cache_ascii_frames(video_path, cache_path, width=120):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("无法打开视频文件")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    ascii_frames = []
    print("开始预计算ASCII帧...")
    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame = image_to_ascii_colored(frame, width)
        ascii_frames.append(ascii_frame)

        if (i + 1) % 100 == 0 or (i + 1) == total_frames:
            print(f"预计算帧: {i + 1}/{total_frames}")

    cap.release()

    with open(cache_path, 'wb') as f:
        pickle.dump(ascii_frames, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"预计算完成，缓存已保存至 {cache_path}")


# 从缓存中加载ASCII帧
def load_ascii_frames(cache_path):
    with open(cache_path, 'rb') as f:
        return pickle.load(f)


# 播放缓存好的ASCII视频
def play_cached_ascii_video(ascii_frames, fps):
    frame_duration = 1 / fps

    # 隐藏光标并清空屏幕
    print(term.hide_cursor() + term.clear())
    try:
        for ascii_frame in ascii_frames:
            start_time = time.time()

            # 使用 blessed 提供的快速刷新功能
            with term.location(0, 0):
                print(ascii_frame)

            # 控制帧率
            elapsed = time.time() - start_time
            sleep_time = frame_duration - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
    except KeyboardInterrupt:
        pass
    finally:
        # 重置颜色并显示光标
        print(term.normal + term.show_cursor())


# 检查是否有缓存文件，如果没有则进行预计算
def play_ascii_video_terminal_with_cache(video_path, cache_path, width=120):
    # 获取视频帧率
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 60  # 默认帧率
    cap.release()

    # 检查缓存文件是否存在
    if not os.path.exists(cache_path):
        print("未找到缓存，开始预计算...")
        cache_ascii_frames(video_path, cache_path, width)

    # 加载缓存
    ascii_frames = load_ascii_frames(cache_path)
    print("缓存加载完成，开始播放...")
    play_cached_ascii_video(ascii_frames, fps)


# 示例使用
if __name__ == "__main__":
    video_path = 'D:\应用\相册\hudiewu.mp4'  # 视频路径
    cache_path = 'ascii_cache.pkl'  # 缓存文件路径
    width = 120  # 根据终端大小调整宽度

    print(term.clear())
    print("开始播放ASCII视频... 按 Ctrl+C 退出")
    play_ascii_video_terminal_with_cache(video_path, cache_path, width)
