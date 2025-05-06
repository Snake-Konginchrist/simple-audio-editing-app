from tkinter import messagebox

def show_error(title, message):
    """
    显示错误消息对话框
    
    参数:
        title: 对话框标题
        message: 错误消息
    """
    messagebox.showerror(title, message)

def show_info(title, message):
    """
    显示信息消息对话框
    
    参数:
        title: 对话框标题
        message: 信息消息
    """
    messagebox.showinfo(title, message)

def show_warning(title, message):
    """
    显示警告消息对话框
    
    参数:
        title: 对话框标题
        message: 警告消息
    """
    messagebox.showwarning(title, message) 