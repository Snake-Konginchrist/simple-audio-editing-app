import tkinter as tk
from tkinter import ttk, StringVar
import os

from src.utils import (
    load_audio_file, 
    format_time, 
    get_audio_duration
)

from .tabs.main_tab import MainTab
from .tabs.cut_tab import CutTab
from .tabs.merge_tab import MergeTab 
from .tabs.effects_tab import EffectsTab

class AudioEditorApp:
    """
    音频编辑器应用主类
    """
    def __init__(self, root):
        """
        初始化应用
        
        参数:
            root: Tkinter根窗口
        """
        self.root = root
        self.root.title("简易音频编辑器")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # 存储当前加载的音频文件路径
        self.current_audio_path = None
        self.audio_duration = 0
        
        # 设置样式
        self.setup_styles()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建界面组件
        self.create_widgets()
    
    def setup_styles(self):
        """
        设置UI样式
        """
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TLabel", background="#f0f0f0")
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
    
    def create_widgets(self):
        """
        创建UI组件
        """
        # 创建标题
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=10)
        
        title_label = ttk.Label(title_frame, text="简易音频编辑器", style="Title.TLabel")
        title_label.pack()
        
        # 创建控制栏框架
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        # 创建一个选项卡控件
        tab_control = ttk.Notebook(self.main_frame)
        
        # 创建各个功能选项卡
        self.main_tab = MainTab(tab_control, self)
        self.cut_tab = CutTab(tab_control, self)
        self.merge_tab = MergeTab(tab_control, self)
        self.effects_tab = EffectsTab(tab_control, self)
        
        # 将选项卡添加到控件
        tab_control.add(self.main_tab.frame, text="基本信息")
        tab_control.add(self.cut_tab.frame, text="剪切/删除")
        tab_control.add(self.merge_tab.frame, text="合并音频")
        tab_control.add(self.effects_tab.frame, text="音频效果")
        
        tab_control.pack(expand=1, fill=tk.BOTH)
        
        # 创建状态栏
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        self.status_var = StringVar()
        self.status_var.set("未加载音频文件")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)
    
    def load_audio(self):
        """
        加载音频文件
        """
        file_path = load_audio_file()
        if file_path:
            self.current_audio_path = file_path
            self.audio_duration = get_audio_duration(file_path)
            
            filename = os.path.basename(file_path)
            duration_str = format_time(self.audio_duration)
            
            self.status_var.set(f"已加载: {filename} (时长: {duration_str})")
            self.main_tab.update_audio_info(file_path, self.audio_duration)
            
            # 更新其他选项卡的信息
            self.cut_tab.update_duration(self.audio_duration)
            
            return True
        return False 