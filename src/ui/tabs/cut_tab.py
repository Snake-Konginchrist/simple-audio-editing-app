import tkinter as tk
from tkinter import ttk, StringVar

from src.utils import (
    format_time, 
    parse_time, 
    save_audio_file, 
    show_error, 
    show_info
)
from src.core import AudioProcessor
from .base_tab import BaseTab

class CutTab(BaseTab):
    """
    剪切/删除选项卡
    """
    def __init__(self, parent, app):
        super().__init__(parent, app)
    
    def create_widgets(self):
        # 剪切部分
        cut_frame = ttk.LabelFrame(self.frame, text="剪切音频", padding="10")
        cut_frame.pack(fill=tk.X, pady=10)
        
        # 范围选择
        range_frame = ttk.Frame(cut_frame)
        range_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(range_frame, text="开始时间:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.start_time_var = StringVar(value="00:00.00")
        start_entry = ttk.Entry(range_frame, textvariable=self.start_time_var, width=10)
        start_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(range_frame, text="结束时间:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.end_time_var = StringVar(value="00:00.00")
        end_entry = ttk.Entry(range_frame, textvariable=self.end_time_var, width=10)
        end_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(range_frame, text="总时长:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.duration_var = StringVar(value="00:00.00")
        duration_label = ttk.Label(range_frame, textvariable=self.duration_var)
        duration_label.grid(row=0, column=5, padx=5, pady=5)
        
        # 按钮
        button_frame = ttk.Frame(cut_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        preview_cut_button = ttk.Button(button_frame, text="预览剪切", command=self.preview_cut)
        preview_cut_button.pack(side=tk.LEFT, padx=5)
        
        cut_button = ttk.Button(button_frame, text="剪切选定部分", command=self.cut_audio)
        cut_button.pack(side=tk.LEFT, padx=5)
        
        preview_remove_button = ttk.Button(button_frame, text="预览删除", command=self.preview_remove)
        preview_remove_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = ttk.Button(button_frame, text="删除选定部分", command=self.remove_segment)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # 说明
        note_label = ttk.Label(
            cut_frame, 
            text="提示: 时间格式为分:秒.毫秒，例如 01:23.45 表示1分23.45秒", 
            font=("Arial", 9, "italic")
        )
        note_label.pack(fill=tk.X, pady=5)
    
    def update_duration(self, duration):
        """
        更新音频时长
        
        参数:
            duration: 音频时长(毫秒)
        """
        self.duration_var.set(format_time(duration))
        # 默认设置结束时间为音频总时长
        self.end_time_var.set(format_time(duration))
    
    def validate_time_range(self):
        """
        验证时间范围
        
        返回:
            成功时返回(start_ms, end_ms)元组，失败返回None
        """
        if not self.app.current_audio_path:
            show_error("错误", "请先加载音频文件")
            return None
        
        try:
            start_ms = parse_time(self.start_time_var.get())
            end_ms = parse_time(self.end_time_var.get())
            
            if start_ms >= end_ms:
                show_error("错误", "开始时间必须小于结束时间")
                return None
            
            return start_ms, end_ms
                
        except Exception as e:
            show_error("错误", f"时间格式错误: {str(e)}")
            return None
    
    def preview_cut(self):
        """
        预览剪切效果
        """
        time_range = self.validate_time_range()
        if not time_range:
            return
            
        start_ms, end_ms = time_range
        
        try:
            # 使用统一的预览接口
            AudioProcessor.preview_operation(
                self.app.current_audio_path,
                AudioProcessor.cut_audio,
                start_ms, end_ms
            )
        except Exception as e:
            show_error("错误", f"预览剪切音频失败: {str(e)}")
    
    def preview_remove(self):
        """
        预览删除效果
        """
        time_range = self.validate_time_range()
        if not time_range:
            return
            
        start_ms, end_ms = time_range
        
        try:
            # 使用统一的预览接口
            AudioProcessor.preview_operation(
                self.app.current_audio_path,
                AudioProcessor.remove_segment,
                start_ms, end_ms
            )
        except Exception as e:
            show_error("错误", f"预览删除效果失败: {str(e)}")
    
    def cut_audio(self):
        """
        剪切音频
        """
        time_range = self.validate_time_range()
        if not time_range:
            return
            
        start_ms, end_ms = time_range
        
        try:
            output_path = save_audio_file()
            if not output_path:
                return
                
            AudioProcessor.cut_audio(self.app.current_audio_path, output_path, start_ms, end_ms)
            show_info("成功", f"已成功剪切音频并保存到: {output_path}")
            
        except Exception as e:
            show_error("错误", f"剪切音频失败: {str(e)}")
    
    def remove_segment(self):
        """
        删除音频片段
        """
        time_range = self.validate_time_range()
        if not time_range:
            return
            
        start_ms, end_ms = time_range
        
        try:
            output_path = save_audio_file()
            if not output_path:
                return
                
            AudioProcessor.remove_segment(self.app.current_audio_path, output_path, start_ms, end_ms)
            show_info("成功", f"已成功删除音频片段并保存到: {output_path}")
            
        except Exception as e:
            show_error("错误", f"删除音频片段失败: {str(e)}") 