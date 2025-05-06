from .app import AudioEditorApp

def create_main_window(root):
    """
    创建主窗口函数 (为了兼容)
    
    参数:
        root: Tkinter根窗口
    """
    return AudioEditorApp(root) 