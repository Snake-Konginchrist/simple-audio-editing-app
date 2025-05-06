import tkinter as tk
from tkinter import ttk, StringVar
import os

from src.utils import format_time
from .base_tab import BaseTab

class MainTab(BaseTab):
    """
    主信息选项卡
    """
    def __init__(self, parent, app):
        super().__init__(parent, app)
    
    def create_widgets(self):
        # 创建加载按钮
        load_button = ttk.Button(self.frame, text="加载音频文件", command=self.app.load_audio)
        load_button.pack(pady=10)
        
        # 添加文件信息区域
        info_frame = ttk.LabelFrame(self.frame, text="音频文件信息", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        # 文件路径
        path_frame = ttk.Frame(info_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(path_frame, text="文件路径:").pack(side=tk.LEFT)
        self.path_var = StringVar()
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, state="readonly", width=50)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 文件格式
        format_frame = ttk.Frame(info_frame)
        format_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(format_frame, text="文件格式:").pack(side=tk.LEFT)
        self.format_var = StringVar()
        format_entry = ttk.Entry(format_frame, textvariable=self.format_var, state="readonly", width=20)
        format_entry.pack(side=tk.LEFT, padx=5)
        
        # 音频时长
        duration_frame = ttk.Frame(info_frame)
        duration_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(duration_frame, text="音频时长:").pack(side=tk.LEFT)
        self.duration_var = StringVar()
        duration_entry = ttk.Entry(duration_frame, textvariable=self.duration_var, state="readonly", width=20)
        duration_entry.pack(side=tk.LEFT, padx=5)
        
        # 添加使用说明
        help_frame = ttk.LabelFrame(self.frame, text="使用说明", padding="10")
        help_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        help_text = """
        1. 首先加载音频文件
        2. 切换到不同的功能选项卡执行对应操作
        3. 剪切/删除: 可以剪取音频的指定部分或删除某段
        4. 合并音频: 选择多个音频文件进行合并
        5. 音频效果: 添加各种音频效果，如倒放、改变速度等
        """
        
        help_label = ttk.Label(help_frame, text=help_text, justify=tk.LEFT)
        help_label.pack(fill=tk.BOTH, expand=True)
    
    def update_audio_info(self, file_path, duration):
        """
        更新音频文件信息
        
        参数:
            file_path: 文件路径
            duration: 音频时长(毫秒)
        """
        self.path_var.set(file_path)
        self.format_var.set(os.path.splitext(file_path)[1].upper())
        self.duration_var.set(format_time(duration)) 