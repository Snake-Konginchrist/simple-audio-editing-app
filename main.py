import tkinter as tk
from src.ui import create_main_window

def main():
    """
    程序主入口函数
    """
    app = tk.Tk()  # 创建一个Tkinter窗口实例
    app.title("简易音频编辑器")  # 设置窗口标题
    
    # 设置应用图标（如果有）
    # app.iconbitmap("icon.ico")
    
    create_main_window(app)  # 调用UI模块，创建主窗口
    app.mainloop()  # 开始Tkinter事件循环，运行程序

# 程序入口
if __name__ == "__main__":
    main()
