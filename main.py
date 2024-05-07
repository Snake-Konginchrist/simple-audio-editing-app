import tkinter as tk
from ui import create_main_window

# 程序入口
if __name__ == "__main__":
    app = tk.Tk()  # 创建一个Tkinter窗口实例
    create_main_window(app)  # 调用UI模块，创建主窗口
    app.mainloop()  # 开始Tkinter事件循环，运行程序
