import tkinter as tk
import os
import sys
import logging
from src.ui import create_main_window

# 配置日志
def setup_logging():
    """
    设置日志系统
    只在非单文件模式下启用日志功能
    """
    # 检查是否为单文件模式（PyInstaller打包）
    is_single_file = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    
    # 单文件模式下不启用日志，直接返回
    if is_single_file:
        # 禁用所有日志
        logging.basicConfig(level=logging.CRITICAL)
        return
    
    # 非单文件模式（开发环境或文件夹模式打包），启用日志
    log_folder = "logs"
    if not os.path.exists(log_folder):
        try:
            os.makedirs(log_folder)
        except:
            # 如果无法创建日志目录，使用当前目录
            log_folder = "."
    
    log_file = os.path.join(log_folder, "app.log")
    
    # 配置日志格式和级别
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # 同时输出到控制台
        ]
    )
    
    # 记录应用启动信息
    logging.info("应用启动")
    logging.info(f"Python版本: {sys.version}")
    logging.info(f"是否打包环境: {getattr(sys, 'frozen', False)}")
    if getattr(sys, 'frozen', False):
        logging.info(f"可执行文件路径: {sys.executable}")
    logging.info(f"工作目录: {os.getcwd()}")

def main():
    """
    程序主入口函数
    """
    # 设置日志
    setup_logging()
    
    app = tk.Tk()  # 创建一个Tkinter窗口实例
    app.title("简易音频编辑器")  # 设置窗口标题
    
    # 设置应用图标
    try:
        # 确定图标文件路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的环境
            application_path = os.path.dirname(sys.executable)
            icon_path = os.path.join(application_path, "icon.ico")
        else:
            # 如果是开发环境
            icon_path = "icon.ico"
        
        # 检查文件是否存在
        if os.path.exists(icon_path):
            app.iconbitmap(icon_path)
    except Exception as e:
        print(f"警告: 无法设置应用图标 - {e}")
    
    create_main_window(app)  # 调用UI模块，创建主窗口
    app.mainloop()  # 开始Tkinter事件循环，运行程序

# 程序入口
if __name__ == "__main__":
    main()
