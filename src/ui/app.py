import tkinter as tk
from tkinter import ttk, StringVar, Menu
import os

from src.utils import (
    load_audio_file, 
    format_time, 
    get_audio_duration
)
from src.utils.language import get_text, set_language
from src.utils.config import get_language
from src.ui.language_switcher import LanguageSwitcher

from .tabs.main_tab import MainTab
from .tabs.cut_tab import CutTab
from .tabs.merge_tab import MergeTab 
from .tabs.effects_tab import EffectsTab
from .tabs.extract_tab import ExtractTab

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
        
        # 初始化语言设置
        set_language(get_language())
        
        self.root.title(get_text("app_title"))
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # 存储当前加载的音频文件路径
        self.current_audio_path = None
        self.audio_duration = 0
        
        # 设置样式
        self.setup_styles()
        
        # 创建菜单栏
        self.create_menu()
        
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
    
    def create_menu(self):
        """
        创建菜单栏
        """
        self.menu_bar = Menu(self.root)
        
        # 文件菜单
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=get_text("file"), menu=file_menu)
        file_menu.add_command(label=get_text("open"), command=self.load_audio)
        file_menu.add_separator()
        file_menu.add_command(label=get_text("exit"), command=self.root.quit)
        
        # 编辑菜单
        edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=get_text("edit"), menu=edit_menu)
        
        # 帮助菜单
        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=get_text("help"), menu=help_menu)
        help_menu.add_command(label=get_text("about"), command=self.show_about)
        
        # 添加语言切换器
        self.lang_switcher = LanguageSwitcher(self.root, self.menu_bar)
        
        # 设置菜单栏
        self.root.config(menu=self.menu_bar)
    
    def create_widgets(self):
        """
        创建UI组件
        """
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
        self.extract_tab = ExtractTab(tab_control, self)
        
        # 将选项卡添加到控件
        tab_control.add(self.main_tab.frame, text=get_text("tab_basic_info"))
        tab_control.add(self.cut_tab.frame, text=get_text("tab_cut_delete"))
        tab_control.add(self.merge_tab.frame, text=get_text("tab_merge"))
        tab_control.add(self.effects_tab.frame, text=get_text("tab_effects"))
        tab_control.add(self.extract_tab.frame, text=get_text("tab_video_extract"))
        
        tab_control.pack(expand=1, fill=tk.BOTH)
        
        # 创建状态栏
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        self.status_var = StringVar()
        self.status_var.set(get_text("no_file_selected"))
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)
        
        # 在状态栏添加语言切换下拉框
        self.lang_switcher.create_language_combobox(status_frame)
    
    def show_about(self):
        """
        显示关于对话框
        """
        from tkinter import messagebox
        messagebox.showinfo(
            get_text("about"),
            f"{get_text('app_title')} v1.0\n"
            f"Copyright © 2023\n\n"
            f"一个简单的桌面音频编辑应用"
        )
    
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
            
            self.status_var.set(f"{get_text('load_audio_file')}: {filename} ({get_text('duration')}: {duration_str})")
            self.main_tab.update_audio_info(file_path, self.audio_duration)
            
            # 更新其他选项卡的信息
            self.cut_tab.update_duration(self.audio_duration)
            
            return True
        return False 