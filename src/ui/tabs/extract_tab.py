import tkinter as tk
from tkinter import ttk, StringVar, IntVar, BooleanVar
import os

from src.utils import (
    load_video_file,
    save_audio_file,
    show_error,
    show_info
)
from src.core import AudioProcessor
from .base_tab import BaseTab

class ExtractTab(BaseTab):
    """
    视频音频提取选项卡
    """
    def __init__(self, parent, app):
        self.video_path = None
        self.video_name = StringVar(value="未选择视频文件")
        self.audio_info = None  # 存储视频音频信息
        self.original_codec = "unknown"  # 原始编码器
        super().__init__(parent, app)
    
    def create_widgets(self):
        # 创建视频提取框架
        extract_frame = ttk.LabelFrame(self.frame, text="从视频中提取音频", padding="10")
        extract_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 视频选择区域
        video_select_frame = ttk.Frame(extract_frame)
        video_select_frame.pack(fill=tk.X, pady=10)
        
        load_button = ttk.Button(video_select_frame, text="选择视频文件", command=self.load_video)
        load_button.pack(side=tk.LEFT, padx=5)
        
        video_label = ttk.Label(video_select_frame, textvariable=self.video_name)
        video_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 音频格式选择
        format_frame = ttk.Frame(extract_frame)
        format_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(format_frame, text="输出格式:").pack(side=tk.LEFT, padx=5)
        
        self.format_var = StringVar(value="mp3")
        formats = ["mp3", "wav", "aac", "ogg", "flac", "m4a"]
        format_combobox = ttk.Combobox(format_frame, textvariable=self.format_var, values=formats, state="readonly", width=10)
        format_combobox.pack(side=tk.LEFT, padx=5)
        format_combobox.bind("<<ComboboxSelected>>", self.check_format_compatibility)
        
        # 音频质量选择
        quality_frame = ttk.Frame(extract_frame)
        quality_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(quality_frame, text="音频质量:").pack(side=tk.LEFT, padx=5)
        
        # 音频质量选择框架
        self.quality_var = StringVar(value="custom")
        
        # 不同质量的单选按钮
        quality_options_frame = ttk.Frame(quality_frame)
        quality_options_frame.pack(fill=tk.X, padx=5)
        
        # 原始音频（不重新编码）
        self.keep_original_radio = ttk.Radiobutton(
            quality_options_frame,
            text="保留原始音频流（不重新编码，需格式兼容）",
            variable=self.quality_var,
            value="original",
            command=self.toggle_bitrate_option
        )
        self.keep_original_radio.grid(row=0, column=0, sticky="w", pady=2)
        
        # 保留原始质量（重新编码）
        ttk.Radiobutton(
            quality_options_frame,
            text="保留原始音频质量（使用原始比特率和采样率）",
            variable=self.quality_var,
            value="original_quality",
            command=self.toggle_bitrate_option
        ).grid(row=1, column=0, sticky="w", pady=2)
        
        # 自定义比特率
        ttk.Radiobutton(
            quality_options_frame,
            text="自定义比特率：",
            variable=self.quality_var,
            value="custom",
            command=self.toggle_bitrate_option
        ).grid(row=2, column=0, sticky="w", pady=2)
        
        # 比特率选择（仅在自定义模式下可用）
        bitrate_frame = ttk.Frame(quality_options_frame)
        bitrate_frame.grid(row=2, column=1, sticky="w", pady=2)
        
        self.bitrate_var = StringVar(value="192k")
        bitrates = ["64k", "128k", "192k", "256k", "320k"]
        self.bitrate_combobox = ttk.Combobox(bitrate_frame, textvariable=self.bitrate_var, values=bitrates, state="readonly", width=10)
        self.bitrate_combobox.pack(side=tk.LEFT)
        
        # 添加兼容性提示
        self.compatibility_var = StringVar(value="")
        compatibility_label = ttk.Label(extract_frame, textvariable=self.compatibility_var, foreground="red")
        compatibility_label.pack(anchor=tk.W, padx=5, pady=2)

        # 视频音频信息显示
        self.audio_info_var = StringVar(value="")
        audio_info_label = ttk.Label(extract_frame, textvariable=self.audio_info_var, justify=tk.LEFT)
        audio_info_label.pack(fill=tk.X, pady=5)
        
        # 提取按钮
        button_frame = ttk.Frame(extract_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        extract_button = ttk.Button(button_frame, text="提取音频", command=self.extract_audio)
        extract_button.pack(side=tk.LEFT, padx=5)
        
        # 提示信息
        info_frame = ttk.Frame(extract_frame)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        info_text = """
        说明:
        1. 选择一个视频文件
        2. 选择输出音频的格式
        3. 选择音频质量选项:
           - 保留原始音频流: 直接复制原音频（无质量损失，但要求格式兼容）
           - 保留原始音频质量: 使用与原音频相同的比特率和采样率（适用于所有格式）
           - 自定义比特率: 手动设置输出音频比特率
        4. 点击"提取音频"按钮
        5. 选择保存位置
        
        支持的视频格式: MP4, AVI, MOV, MKV, FLV, WMV, WebM
        支持的音频格式: MP3, WAV, AAC, OGG, FLAC, M4A
        
        注意: 此功能需要安装FFmpeg
        """
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(fill=tk.X, pady=5)
        
        # 进度显示
        self.status_var = StringVar(value="")
        status_label = ttk.Label(extract_frame, textvariable=self.status_var)
        status_label.pack(fill=tk.X, pady=5)
    
    def check_format_compatibility(self, event=None):
        """
        检查所选格式是否与原始编码器兼容
        """
        if self.original_codec == "unknown":
            return
            
        target_format = self.format_var.get()
        is_compatible = AudioProcessor._is_format_compatible(self.original_codec, target_format)
        
        if not is_compatible:
            self.compatibility_var.set(f"注意: 输出格式{target_format}与原始编码器{self.original_codec}不兼容，无法使用'保留原始音频流'选项")
            self.keep_original_radio.configure(state=tk.DISABLED)
            # 如果当前选择了original但不兼容，则改为original_quality
            if self.quality_var.get() == "original":
                self.quality_var.set("original_quality")
                self.toggle_bitrate_option()
        else:
            self.compatibility_var.set("")
            self.keep_original_radio.configure(state=tk.NORMAL)
    
    def toggle_bitrate_option(self):
        """
        根据质量选项切换比特率选择的可用状态
        """
        if self.quality_var.get() == "custom":
            self.bitrate_combobox.configure(state="readonly")
        else:
            self.bitrate_combobox.configure(state="disabled")
    
    def load_video(self):
        """
        加载视频文件
        """
        video_path = load_video_file()
        if video_path:
            self.video_path = video_path
            self.video_name.set(os.path.basename(video_path))
            self.status_var.set("已选择视频文件，准备提取")
            
            # 获取视频音频信息
            self.audio_info = AudioProcessor.get_video_audio_info(video_path)
            self.original_codec = self.audio_info['codec_name']
            
            # 更新显示
            info_text = f"音频信息: "
            if self.audio_info['codec_name'] != 'unknown':
                info_text += f"编码器: {self.audio_info['codec_name']}, "
            if self.audio_info['bit_rate'] != 'unknown':
                bit_rate_kb = int(int(self.audio_info['bit_rate']) / 1000)
                info_text += f"比特率: {bit_rate_kb}k, "
            if self.audio_info['sample_rate'] != 'unknown':
                info_text += f"采样率: {self.audio_info['sample_rate']}Hz, "
            if self.audio_info['channels'] != 'unknown':
                info_text += f"声道数: {self.audio_info['channels']}"
                
            self.audio_info_var.set(info_text.strip(", "))
            
            # 默认选择自定义比特率
            self.quality_var.set("custom")
            self.toggle_bitrate_option()
            
            # 检查格式兼容性
            self.check_format_compatibility()
    
    def extract_audio(self):
        """
        从视频中提取音频
        """
        if not self.video_path:
            show_error("错误", "请先选择视频文件")
            return
        
        try:
            # 获取选定的格式
            audio_format = self.format_var.get()
            
            # 根据质量选项设置比特率
            quality_option = self.quality_var.get()
            if quality_option == "original":
                audio_bitrate = "original"
            elif quality_option == "original_quality":
                audio_bitrate = "original_quality"
            else:  # custom
                audio_bitrate = self.bitrate_var.get()
            
            # 选择保存位置
            default_ext = f".{audio_format}"
            output_path = save_audio_file(default_ext)
            if not output_path:
                return
            
            # 更新状态
            self.status_var.set("正在提取音频，请稍候...")
            self.frame.update()  # 更新UI
            
            # 提取音频
            success = AudioProcessor.extract_audio_from_video(
                self.video_path, 
                output_path, 
                audio_format, 
                audio_bitrate
            )
            
            if success:
                show_info("成功", f"音频提取成功并保存到:\n{output_path}")
                self.status_var.set("音频提取成功")
            else:
                # 如果FFmpeg失败，尝试使用pydub
                backup_success = AudioProcessor.extract_audio_with_pydub(self.video_path, output_path)
                if backup_success:
                    show_info("成功", f"音频提取成功并保存到:\n{output_path}")
                    self.status_var.set("音频提取成功（使用备用方法）")
                else:
                    show_error("错误", "无法提取音频。请确保已正确安装FFmpeg并添加到系统路径。")
                    self.status_var.set("音频提取失败")
        
        except Exception as e:
            show_error("错误", f"提取音频时出错: {str(e)}")
            self.status_var.set("音频提取失败") 