#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语言切换器组件 - 提供切换应用界面语言的功能
适配基于JSON的翻译系统
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import subprocess

from src.utils.language import get_text, set_language, get_supported_languages
from src.utils.config import get_language, set_language as save_language


class LanguageSwitcher:
    """语言切换器组件，提供语言切换菜单选项"""
    
    def __init__(self, parent, menu=None):
        """
        初始化语言切换器
        
        参数:
            parent: 父窗口
            menu: 菜单对象，如果提供，则添加语言切换选项到此菜单
        """
        self.parent = parent
        self.current_language = get_language()
        
        # 获取支持的语言列表
        self.supported_languages = get_supported_languages()
        
        if menu:
            self.create_language_menu(menu)
    
    def create_language_menu(self, parent_menu):
        """创建语言菜单"""
        # 创建语言子菜单
        language_menu = tk.Menu(parent_menu, tearoff=0)
        parent_menu.add_cascade(label=get_text("language"), menu=language_menu)
        
        # 当前选择的语言
        self.lang_var = tk.StringVar(value=self.current_language)
        
        # 为每种支持的语言添加单选按钮
        for lang_code, lang_name in self.supported_languages.items():
            language_menu.add_radiobutton(
                label=lang_name,
                variable=self.lang_var,
                value=lang_code,
                command=lambda code=lang_code: self.switch_language(code)
            )
        
        return language_menu
    
    def create_language_combobox(self, parent_frame):
        """创建语言下拉选择框"""
        # 创建标签
        label = ttk.Label(parent_frame, text=get_text("language") + ":")
        label.pack(side=tk.LEFT, padx=(5, 2))
        
        # 语言显示名称列表
        lang_names = list(self.supported_languages.values())
        
        # 创建下拉框
        self.language_combo = ttk.Combobox(
            parent_frame,
            values=lang_names,
            state="readonly",
            width=15
        )
        
        # 设置当前值
        for i, lang_code in enumerate(self.supported_languages.keys()):
            if lang_code == self.current_language:
                self.language_combo.current(i)
                break
        
        self.language_combo.pack(side=tk.LEFT, padx=(2, 5))
        
        # 绑定选择事件
        self.language_combo.bind("<<ComboboxSelected>>", self.on_language_selected)
        
        return self.language_combo
    
    def on_language_selected(self, event):
        """处理下拉框选择事件"""
        selected_index = self.language_combo.current()
        if selected_index >= 0:
            lang_codes = list(self.supported_languages.keys())
            selected_lang = lang_codes[selected_index]
            self.switch_language(selected_lang)
    
    def switch_language(self, language):
        """
        切换应用语言
        
        参数:
            language: 目标语言代码
        """
        if language == self.current_language:
            return  # 如果语言没有变化，不做任何操作
        
        # 保存新的语言设置
        save_language(language)
        self.current_language = language
        
        # 询问用户是否要立即重启应用
        if messagebox.askyesno(
            get_text("restart_required"),
            get_text("language_changed"),
            icon=messagebox.QUESTION
        ):
            self.restart_application()
    
    def restart_application(self):
        """重启应用"""
        # 获取当前脚本的路径
        python = sys.executable
        script = os.path.abspath(sys.argv[0])
        args = sys.argv[1:]
        
        # 关闭当前应用
        self.parent.destroy()
        
        # 启动新的应用实例
        subprocess.Popen([python, script] + args) 