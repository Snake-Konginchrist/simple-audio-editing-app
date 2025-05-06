import tkinter as tk
from tkinter import ttk

class BaseTab:
    """
    选项卡基类
    """
    def __init__(self, parent, app):
        """
        初始化基类
        
        参数:
            parent: 父级容器
            app: 应用实例引用
        """
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent, padding="10")
        self.create_widgets()
    
    def create_widgets(self):
        """
        创建UI组件，子类需重写此方法
        """
        pass 