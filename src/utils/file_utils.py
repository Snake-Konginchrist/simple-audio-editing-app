import os
from tkinter import filedialog
import time
from pydub import AudioSegment
from .message_utils import show_error

def format_time(milliseconds):
    """
    将毫秒转换为易读的时间格式 (分:秒.毫秒)
    
    参数:
        milliseconds: 毫秒数
        
    返回:
        格式化的时间字符串
    """
    seconds = milliseconds / 1000
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:05.2f}"

def parse_time(time_str):
    """
    将时间字符串转换为毫秒
    
    参数:
        time_str: 时间字符串，格式为 "分:秒.毫秒" 或 "秒.毫秒"
        
    返回:
        毫秒数
    """
    try:
        if ":" in time_str:
            minutes, seconds = time_str.split(":")
            return (int(minutes) * 60 + float(seconds)) * 1000
        else:
            return float(time_str) * 1000
    except ValueError:
        from .message_utils import show_error
        show_error("格式错误", "时间格式错误，请使用分:秒.毫秒 或 秒.毫秒 格式")
        return 0

def load_audio_file():
    """
    选择音频文件
    
    返回:
        所选音频文件的路径
    """
    filetypes = [
        ('音频文件', '*.mp3 *.wav *.aac *.ogg *.flac *.m4a'),
        ('所有文件', '*.*')
    ]
    file_path = filedialog.askopenfilename(
        title="选择音频文件",
        filetypes=filetypes
    )
    return file_path

def load_multiple_audio_files():
    """
    选择多个音频文件
    
    返回:
        所选音频文件的路径列表
    """
    filetypes = [
        ('音频文件', '*.mp3 *.wav *.aac *.ogg *.flac *.m4a'),
        ('所有文件', '*.*')
    ]
    file_paths = filedialog.askopenfilenames(
        title="选择多个音频文件",
        filetypes=filetypes
    )
    return file_paths

def save_audio_file(default_ext=".mp3"):
    """
    选择保存音频文件的位置
    
    参数:
        default_ext: 默认文件扩展名
        
    返回:
        保存文件的路径
    """
    filetypes = [
        ('MP3文件', '*.mp3'),
        ('WAV文件', '*.wav'),
        ('AAC文件', '*.aac'),
        ('OGG文件', '*.ogg'),
        ('FLAC文件', '*.flac'),
        ('M4A文件', '*.m4a'),
        ('所有文件', '*.*')
    ]
    
    # 生成默认文件名，使用当前时间戳
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    default_filename = f"audio_edit_{timestamp}{default_ext}"
    
    file_path = filedialog.asksaveasfilename(
        title="保存音频文件",
        filetypes=filetypes,
        defaultextension=default_ext,
        initialfile=default_filename
    )
    return file_path

def get_audio_duration(file_path):
    """
    获取音频文件的时长
    
    参数:
        file_path: 音频文件路径
        
    返回:
        音频时长(毫秒)
    """
    try:
        # 根据文件扩展名判断格式
        ext = os.path.splitext(file_path)[1].lower().strip('.')
        audio = AudioSegment.from_file(file_path, format=ext)
        return len(audio)
    except Exception as e:
        show_error("错误", f"无法获取音频时长: {str(e)}")
        return 0 