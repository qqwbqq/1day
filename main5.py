import tkinter as tk
from PIL import Image, ImageTk


def create_image_gradient_button(root):
    # 创建一个指定大小的图片（这里示例宽度100，高度30，可根据按钮大小调整）
    image = Image.new('RGB', (100, 30), color='#90EE90')  # 初始颜色可以自行设定，这里还是用较浅绿示例
    pixels = image.load()

    # 实现简单的垂直方向颜色渐变（从浅绿到深绿，你可以调整颜色取值范围来改变渐变效果）
    for y in range(image.size[1]):
        r = int(144 - (144 - 0) * y / image.size[1])  # 红色通道值渐变
        g = int(238 - (238 - 0) * y / image.size[1])  # 绿色通道值渐变
        b = int(144 - (144 - 0) * y / image.size[1])  # 蓝色通道值渐变
        for x in range(image.size[0]):
            pixels[x, y] = (r, g, b)

    photo = ImageTk.PhotoImage(image)
    button = tk.Button(root, image=photo, text="渐变按钮", compound=tk.CENTER, bd=0)
    button.image = photo  # 需保留对图片对象的引用，防止被垃圾回收
    button.pack(pady=20)


root = tk.Tk()
root.title("渐变按钮示例")
root.geometry("200x150")

create_image_gradient_button(root)

root.mainloop()
