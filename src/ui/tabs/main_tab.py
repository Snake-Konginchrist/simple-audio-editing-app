import tkinter as tk
from tkinter import ttk, StringVar
import os

from src.utils import format_time
from src.core import AudioProcessor
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
        
        # 添加预览按钮
        preview_frame = ttk.Frame(info_frame)
        preview_frame.pack(fill=tk.X, pady=10)
        
        preview_button = ttk.Button(preview_frame, text="预览原始音频", command=self.preview_audio)
        preview_button.pack(side=tk.LEFT, padx=5)
        
        # 部分预览功能
        ttk.Label(preview_frame, text="预览片段:").pack(side=tk.LEFT, padx=(20, 5))
        self.preview_start_var = StringVar(value="00:00.00")
        preview_start_entry = ttk.Entry(preview_frame, textvariable=self.preview_start_var, width=10)
        preview_start_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(preview_frame, text="至").pack(side=tk.LEFT)
        self.preview_end_var = StringVar(value="00:10.00")
        preview_end_entry = ttk.Entry(preview_frame, textvariable=self.preview_end_var, width=10)
        preview_end_entry.pack(side=tk.LEFT, padx=5)
        
        preview_part_button = ttk.Button(preview_frame, text="预览片段", command=self.preview_part)
        preview_part_button.pack(side=tk.LEFT, padx=5)
        
        # 添加使用说明
        help_frame = ttk.LabelFrame(self.frame, text="使用说明", padding="10")
        help_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        help_text = """
        1. 首先加载音频文件
        2. 可以在此页面预览原始音频或特定片段
        3. 切换到不同的功能选项卡执行对应操作
        4. 剪切/删除: 可以剪取音频的指定部分或删除某段
        5. 合并音频: 选择多个音频文件进行合并，可在文件间添加间隙
        6. 音频效果: 添加各种音频效果，如倒放、改变速度等
        
        所有操作都支持预览功能，让您在保存前确认效果
        """
        
        help_label = ttk.Label(help_frame, text=help_text, justify=tk.LEFT)
        help_label.pack(fill=tk.BOTH, expand=True)
    
    def preview_audio(self):
        """
        预览当前加载的音频
        """
        if not self.app.current_audio_path:
            from src.utils import show_error
            show_error("错误", "请先加载音频文件")
            return
            
        # 直接调用预览功能
        AudioProcessor.preview_audio(self.app.current_audio_path)
    
    def preview_part(self):
        """
        预览音频的指定片段
        """
        if not self.app.current_audio_path:
            from src.utils import show_error
            show_error("错误", "请先加载音频文件")
            return
            
        try:
            from src.utils import parse_time, show_error
            
            start_ms = parse_time(self.preview_start_var.get())
            end_ms = parse_time(self.preview_end_var.get())
            
            if start_ms >= end_ms:
                show_error("错误", "开始时间必须小于结束时间")
                return
                
            # 计算时长
            duration_ms = end_ms - start_ms
            
            # 直接调用预览方法
            AudioProcessor.preview_audio(self.app.current_audio_path, start_ms, duration_ms)
            
        except Exception as e:
            from src.utils import show_error
            show_error("错误", f"预览音频片段失败: {str(e)}")
    
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
        
        # 更新预览结束时间，默认为前10秒或全部
        if duration > 10000:  # 如果超过10秒
            self.preview_end_var.set("00:10.00")
        else:
            self.preview_end_var.set(format_time(duration)) 