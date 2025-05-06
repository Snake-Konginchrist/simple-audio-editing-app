import tkinter as tk
from tkinter import ttk
import os

from src.utils import (
    load_multiple_audio_files, 
    save_audio_file, 
    show_error, 
    show_info
)
from src.core import AudioProcessor
from .base_tab import BaseTab

class MergeTab(BaseTab):
    """
    合并音频选项卡
    """
    def __init__(self, parent, app):
        self.audio_files = []
        super().__init__(parent, app)
    
    def create_widgets(self):
        # 合并部分
        merge_frame = ttk.LabelFrame(self.frame, text="合并多个音频文件", padding="10")
        merge_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 按钮
        button_frame = ttk.Frame(merge_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        add_button = ttk.Button(button_frame, text="添加音频文件", command=self.add_files)
        add_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="清空列表", command=self.clear_files)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        merge_button = ttk.Button(button_frame, text="合并选定文件", command=self.merge_files)
        merge_button.pack(side=tk.LEFT, padx=5)
        
        # 文件列表
        list_frame = ttk.Frame(merge_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(list_frame, text="待合并文件列表:").pack(anchor=tk.W)
        
        # 创建列表框架和滚动条
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set, selectmode=tk.EXTENDED)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.files_listbox.yview)
        
        # 操作按钮
        action_frame = ttk.Frame(merge_frame)
        action_frame.pack(fill=tk.X, pady=5)
        
        move_up_button = ttk.Button(action_frame, text="上移", command=self.move_up)
        move_up_button.pack(side=tk.LEFT, padx=5)
        
        move_down_button = ttk.Button(action_frame, text="下移", command=self.move_down)
        move_down_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = ttk.Button(action_frame, text="移除所选", command=self.remove_selected)
        remove_button.pack(side=tk.LEFT, padx=5)
    
    def add_files(self):
        """
        添加音频文件到列表
        """
        files = load_multiple_audio_files()
        if files:
            for file in files:
                if file not in self.audio_files:
                    self.audio_files.append(file)
                    self.files_listbox.insert(tk.END, os.path.basename(file))
    
    def clear_files(self):
        """
        清空文件列表
        """
        self.audio_files = []
        self.files_listbox.delete(0, tk.END)
    
    def remove_selected(self):
        """
        移除选定的文件
        """
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            return
            
        # 从后往前删除，避免索引变化
        for i in sorted(selected_indices, reverse=True):
            del self.audio_files[i]
            self.files_listbox.delete(i)
    
    def move_up(self):
        """
        上移选定文件
        """
        selected_indices = self.files_listbox.curselection()
        if not selected_indices or selected_indices[0] == 0:
            return
            
        idx = selected_indices[0]
        # 交换列表中的项
        self.audio_files[idx], self.audio_files[idx-1] = self.audio_files[idx-1], self.audio_files[idx]
        
        # 更新界面
        file_name = self.files_listbox.get(idx)
        self.files_listbox.delete(idx)
        self.files_listbox.insert(idx-1, file_name)
        self.files_listbox.selection_clear(0, tk.END)
        self.files_listbox.selection_set(idx-1)
    
    def move_down(self):
        """
        下移选定文件
        """
        selected_indices = self.files_listbox.curselection()
        if not selected_indices or selected_indices[0] == len(self.audio_files) - 1:
            return
            
        idx = selected_indices[0]
        # 交换列表中的项
        self.audio_files[idx], self.audio_files[idx+1] = self.audio_files[idx+1], self.audio_files[idx]
        
        # 更新界面
        file_name = self.files_listbox.get(idx)
        self.files_listbox.delete(idx)
        self.files_listbox.insert(idx+1, file_name)
        self.files_listbox.selection_clear(0, tk.END)
        self.files_listbox.selection_set(idx+1)
    
    def merge_files(self):
        """
        合并选定的音频文件
        """
        if not self.audio_files:
            show_error("错误", "请先添加音频文件")
            return
            
        try:
            output_path = save_audio_file()
            if not output_path:
                return
                
            AudioProcessor.merge_audios(self.audio_files, output_path)
            show_info("成功", f"已成功合并音频并保存到: {output_path}")
            
        except Exception as e:
            show_error("错误", f"合并音频失败: {str(e)}") 