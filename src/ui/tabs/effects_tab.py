import tkinter as tk
from tkinter import ttk, DoubleVar, IntVar

from src.utils import (
    save_audio_file, 
    show_error, 
    show_info
)
from src.core import AudioProcessor
from .base_tab import BaseTab

class EffectsTab(BaseTab):
    """
    音频效果选项卡
    """
    def __init__(self, parent, app):
        super().__init__(parent, app)
    
    def create_widgets(self):
        # 音频效果框架
        effects_frame = ttk.LabelFrame(self.frame, text="音频效果", padding="10")
        effects_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 倒放
        reverse_frame = ttk.Frame(effects_frame)
        reverse_frame.pack(fill=tk.X, pady=5)
        
        reverse_button = ttk.Button(reverse_frame, text="倒放音频", command=self.reverse_audio)
        reverse_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(reverse_frame, text="将音频从后向前播放").pack(side=tk.LEFT, padx=5)
        
        # 调整音量
        volume_frame = ttk.Frame(effects_frame)
        volume_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(volume_frame, text="音量调整(dB):").pack(side=tk.LEFT, padx=5)
        self.volume_var = DoubleVar(value=0.0)
        volume_scale = ttk.Scale(volume_frame, from_=-20, to=20, orient=tk.HORIZONTAL, variable=self.volume_var)
        volume_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        volume_label = ttk.Label(volume_frame, textvariable=self.volume_var)
        volume_label.pack(side=tk.LEFT, padx=5)
        
        volume_button = ttk.Button(volume_frame, text="应用", command=self.adjust_volume)
        volume_button.pack(side=tk.LEFT, padx=5)
        
        # 改变速度
        speed_frame = ttk.Frame(effects_frame)
        speed_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(speed_frame, text="播放速度:").pack(side=tk.LEFT, padx=5)
        self.speed_var = DoubleVar(value=1.0)
        speed_scale = ttk.Scale(speed_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL, variable=self.speed_var)
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        speed_label = ttk.Label(speed_frame, textvariable=self.speed_var)
        speed_label.pack(side=tk.LEFT, padx=5)
        
        speed_button = ttk.Button(speed_frame, text="应用", command=self.change_speed)
        speed_button.pack(side=tk.LEFT, padx=5)
        
        # 淡入淡出
        fade_frame = ttk.Frame(effects_frame)
        fade_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fade_frame, text="淡入/淡出时长(毫秒):").pack(side=tk.LEFT, padx=5)
        self.fade_var = IntVar(value=1000)
        fade_entry = ttk.Entry(fade_frame, textvariable=self.fade_var, width=8)
        fade_entry.pack(side=tk.LEFT, padx=5)
        
        fade_in_button = ttk.Button(fade_frame, text="应用淡入", command=self.apply_fade_in)
        fade_in_button.pack(side=tk.LEFT, padx=5)
        
        fade_out_button = ttk.Button(fade_frame, text="应用淡出", command=self.apply_fade_out)
        fade_out_button.pack(side=tk.LEFT, padx=5)
    
    def reverse_audio(self):
        """
        倒放音频
        """
        if not self.app.current_audio_path:
            show_error("错误", "请先加载音频文件")
            return
            
        try:
            output_path = save_audio_file()
            if not output_path:
                return
                
            AudioProcessor.reverse_audio(self.app.current_audio_path, output_path)
            show_info("成功", f"已成功倒放音频并保存到: {output_path}")
            
        except Exception as e:
            show_error("错误", f"倒放音频失败: {str(e)}")
    
    def adjust_volume(self):
        """
        调整音频音量
        """
        if not self.app.current_audio_path:
            show_error("错误", "请先加载音频文件")
            return
            
        try:
            output_path = save_audio_file()
            if not output_path:
                return
                
            AudioProcessor.adjust_volume(self.app.current_audio_path, output_path, self.volume_var.get())
            show_info("成功", f"已成功调整音频音量并保存到: {output_path}")
            
        except Exception as e:
            show_error("错误", f"调整音频音量失败: {str(e)}")
    
    def change_speed(self):
        """
        改变音频速度
        """
        if not self.app.current_audio_path:
            show_error("错误", "请先加载音频文件")
            return
            
        try:
            output_path = save_audio_file()
            if not output_path:
                return
                
            AudioProcessor.change_speed(self.app.current_audio_path, output_path, self.speed_var.get())
            show_info("成功", f"已成功改变音频速度并保存到: {output_path}")
            
        except Exception as e:
            show_error("错误", f"改变音频速度失败: {str(e)}")
    
    def apply_fade_in(self):
        """
        应用淡入效果
        """
        if not self.app.current_audio_path:
            show_error("错误", "请先加载音频文件")
            return
            
        try:
            output_path = save_audio_file()
            if not output_path:
                return
                
            AudioProcessor.fade_in(self.app.current_audio_path, output_path, self.fade_var.get())
            show_info("成功", f"已成功应用淡入效果并保存到: {output_path}")
            
        except Exception as e:
            show_error("错误", f"应用淡入效果失败: {str(e)}")
    
    def apply_fade_out(self):
        """
        应用淡出效果
        """
        if not self.app.current_audio_path:
            show_error("错误", "请先加载音频文件")
            return
            
        try:
            output_path = save_audio_file()
            if not output_path:
                return
                
            AudioProcessor.fade_out(self.app.current_audio_path, output_path, self.fade_var.get())
            show_info("成功", f"已成功应用淡出效果并保存到: {output_path}")
            
        except Exception as e:
            show_error("错误", f"应用淡出效果失败: {str(e)}") 