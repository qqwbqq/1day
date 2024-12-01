from tkinter import *
import pyautogui
import pyperclip
import time

def gg(text, time_1, number):
    time.sleep(2)  # 等待时间
    for i in text.split("\n"):  # 使用正确的换行符分割字符串
        for _ in range(number):  # 使用 number 控制发送次数
            print(i)
            pyperclip.copy(i)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.typewrite("\n")
            time.sleep(time_1)

def open():
    text = z.get()
    time_1 = float(x.get())
    number = int(c.get())
    gg(text, time_1, number)

root = Tk()
root.config(bg='#ffc0cb')
root.title("小清的懒人发泡机!")
root.geometry('450x260+700+300')

Label(root, text="语句：").place(x=5, y=25, width=90, height=40)
z = Entry(root)
z.place(x=100, y=25, width=340, height=40)

Label(root, text="语速：").place(x=5, y=85, width=90, height=40)
x = Entry(root)
x.place(x=100, y=85, width=340, height=40)

Label(root, text="次数：").place(x=5, y=145, width=90, height=40)
c = Entry(root)
c.place(x=100, y=145, width=340, height=40)

Button(root, text="确认", bg='#7CCD7C', height=40, width=90, command=open).place(x=230, y=205, width=200, height=40)
Label(root, text="准备时间2秒！").place(x=20, y=205, width=180, height=40)

root.resizable(0, 0)  # 固定窗口
root.mainloop()  # 显示窗口