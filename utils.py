import os
from tkinter import filedialog


def load_file():
    # 选择文件的函数
    file_path = filedialog.askopenfilename()  # 打开文件选择对话框
    return file_path


def save_file(input_file):
    # 根据加载的文件确定扩展名
    file_ext = os.path.splitext(input_file)[1]  # 从输入文件路径提取文件扩展名
    options = {
        'defaultextension': file_ext,
        'filetypes': [(f'{file_ext} 文件', f'*{file_ext}'),('All files', '.*')],
        'title': '另存为'
    }
    # 保存文件的函数，使用输入文件的扩展名作为默认扩展名
    file_path = filedialog.asksaveasfilename(**options)
    return file_path
