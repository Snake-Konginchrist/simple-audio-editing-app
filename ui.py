import tkinter as tk

from processors import reverse_audio, reverse_video
from utils import load_file, save_file


def process_file(status_label):
    # 处理文件的函数
    input_path = load_file()  # 使用utils模块的函数选择文件
    if not input_path:
        return

    output_path = save_file(input_path)  # 使用utils模块的函数保存文件
    if not output_path:
        return

    # 根据文件类型调用相应的处理函数
    if input_path.lower().endswith(('.mp3', '.wav')):
        reverse_audio(input_path, output_path)
        status_label.config(text="音频已倒放并保存！")
    elif input_path.lower().endswith(('.mp4', '.avi')):
        reverse_video(input_path, output_path)
        status_label.config(text="视频已倒放并保存！")
    else:
        status_label.config(text="不支持的文件格式！")


def create_main_window(app):
    app.title("倒放音视频应用")  # 创建主窗口的函数
    app.geometry('300x100')  # 设置窗口大小为 800x600 像素

    frame = tk.Frame(app)
    frame.pack(pady=20)

    # 创建按钮和状态标签
    button = tk.Button(frame, text="上传并倒放音频/视频", command=lambda: process_file(status_label))
    button.pack(pady=10)

    status_label = tk.Label(frame, text="")
    status_label.pack(pady=10)
