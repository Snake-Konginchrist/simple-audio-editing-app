#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语言工具模块 - 提供多语言支持
从JSON文件读取界面文本资源
"""

import os
import sys
import json
import logging
from pathlib import Path

# 支持的语言
LANGUAGE_CHINESE = "zh_CN"
LANGUAGE_ENGLISH = "en_US"

# 默认语言
DEFAULT_LANGUAGE = LANGUAGE_CHINESE

# 判断是否为单文件模式
def is_single_file_mode():
    """检查是否为PyInstaller单文件打包模式"""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

# 有条件地记录日志
def log_info(message):
    """根据打包模式记录信息日志"""
    if not is_single_file_mode():
        logging.info(message)

def log_error(message):
    """根据打包模式记录错误日志"""
    if not is_single_file_mode():
        logging.error(message)

# 获取应用根目录（处理打包情况）
def get_application_root():
    """获取应用程序根目录，兼容开发环境和打包环境"""
    if getattr(sys, 'frozen', False):
        # 打包环境
        # 对于单文件模式，PyInstaller使用_MEIPASS环境变量指向临时解压目录
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        # 对于目录模式
        return os.path.dirname(sys.executable)
    else:
        # 开发环境
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 翻译文件目录
def get_locale_dir():
    """获取本地化文件目录，兼容开发环境和打包环境"""
    if getattr(sys, 'frozen', False):
        # 打包环境
        # 对于单文件模式，PyInstaller会将资源解压到临时目录
        if hasattr(sys, '_MEIPASS'):
            # 尝试多个可能的路径
            possible_paths = [
                os.path.join(sys._MEIPASS, "src", "locales"),
                os.path.join(sys._MEIPASS, "locales"),
                # 直接在临时目录中查找
                os.path.join(sys._MEIPASS)
            ]
            
            # 调试信息
            for path in possible_paths:
                if os.path.exists(path):
                    log_info(f"找到翻译目录: {path}")
                    # 列出目录内容
                    try:
                        files = os.listdir(path)
                        log_info(f"目录内容: {files}")
                    except Exception as e:
                        log_error(f"无法列出目录内容: {e}")
            
            # 返回第一个存在的路径
            for path in possible_paths:
                if os.path.exists(path):
                    # 检查是否包含翻译文件
                    for lang in SUPPORTED_LANGUAGES.keys():
                        if os.path.exists(os.path.join(path, f"{lang}.json")):
                            return path
            
            # 如果直接找不到目录，尝试在临时目录中搜索文件
            for root, dirs, files in os.walk(sys._MEIPASS):
                for file in files:
                    if file.endswith('.json') and file.split('.')[0] in SUPPORTED_LANGUAGES:
                        return os.path.dirname(os.path.join(root, file))
            
            # 都找不到，使用默认路径
            return os.path.join(sys._MEIPASS, "src", "locales")
        else:
            # 目录模式
            root_dir = os.path.dirname(sys.executable)
            candidate_dirs = [
                os.path.join(root_dir, "locales"),
                os.path.join(root_dir, "src", "locales")
            ]
            for dir_path in candidate_dirs:
                if os.path.exists(dir_path):
                    return dir_path
            return candidate_dirs[0]  # 返回第一个作为默认值
    else:
        # 开发环境
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "locales")

# 支持的语言及其显示名称
SUPPORTED_LANGUAGES = {
    LANGUAGE_CHINESE: "简体中文",
    LANGUAGE_ENGLISH: "English"
}


class LanguageManager:
    """语言管理器，用于获取不同语言的文本"""
    
    def __init__(self, language=DEFAULT_LANGUAGE):
        """初始化语言管理器"""
        self.language = language
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """加载所有支持语言的翻译文件"""
        self.translations = {}
        locale_dir = get_locale_dir()
        log_info(f"翻译文件目录: {locale_dir}")
        
        # 检查翻译目录是否存在
        if not os.path.exists(locale_dir):
            log_error(f"翻译目录不存在: {locale_dir}")
            # 在打包环境中，尝试查找文件
            if getattr(sys, 'frozen', False):
                log_info("在打包环境中尝试查找翻译文件")
                if hasattr(sys, '_MEIPASS'):
                    # 列出_MEIPASS目录内容以便调试
                    try:
                        log_info(f"_MEIPASS目录: {sys._MEIPASS}")
                        for root, dirs, files in os.walk(sys._MEIPASS):
                            log_info(f"目录: {root}")
                            log_info(f"子目录: {dirs}")
                            log_info(f"文件: {files}")
                    except Exception as e:
                        log_error(f"遍历_MEIPASS目录失败: {e}")
        
        for lang_code in SUPPORTED_LANGUAGES.keys():
            try:
                # 构建翻译文件路径
                translation_file = os.path.join(locale_dir, f"{lang_code}.json")
                
                # 如果在指定目录中找不到，尝试在打包环境中查找
                if not os.path.exists(translation_file) and getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                    # 在临时目录中递归查找
                    for root, dirs, files in os.walk(sys._MEIPASS):
                        if f"{lang_code}.json" in files:
                            translation_file = os.path.join(root, f"{lang_code}.json")
                            log_info(f"在临时目录中找到翻译文件: {translation_file}")
                            break
                
                # 读取翻译文件
                if os.path.exists(translation_file):
                    with open(translation_file, 'r', encoding='utf-8') as file:
                        self.translations[lang_code] = json.load(file)
                    log_info(f"已加载{lang_code}语言文件: {translation_file}")
                else:
                    log_error(f"找不到{lang_code}语言文件: {translation_file}")
            except Exception as e:
                log_error(f"加载{lang_code}语言文件失败: {e}")
                # 如果加载失败，使用空字典
                self.translations[lang_code] = {}
    
    def set_language(self, language):
        """设置当前语言"""
        if language in SUPPORTED_LANGUAGES:
            self.language = language
            return True
        return False
    
    def get_text(self, key, default=None):
        """获取指定键的文本，如果不存在则返回默认值或键名"""
        # 确保翻译字典已加载
        if not self.translations:
            self.load_translations()
        
        # 获取当前语言的翻译
        lang_dict = self.translations.get(self.language, {})
        
        # 如果在当前语言中找到翻译，则返回
        if key in lang_dict:
            return lang_dict[key]
        
        # 否则尝试从默认语言获取
        if self.language != DEFAULT_LANGUAGE and DEFAULT_LANGUAGE in self.translations:
            default_dict = self.translations[DEFAULT_LANGUAGE]
            if key in default_dict:
                return default_dict[key]
        
        # 如果都没找到，返回默认值或键名
        return default if default is not None else key


# 创建一个全局的语言管理器实例
_language_manager = None

def get_language_manager():
    """获取或创建语言管理器实例"""
    global _language_manager
    if _language_manager is None:
        from src.utils.config import get_language
        _language_manager = LanguageManager(get_language())
    return _language_manager

def get_text(key, default=None):
    """获取当前语言下指定键的文本"""
    return get_language_manager().get_text(key, default)

def set_language(language):
    """设置当前语言"""
    return get_language_manager().set_language(language)

def get_supported_languages():
    """获取支持的语言列表"""
    return SUPPORTED_LANGUAGES

def reload_translations():
    """重新加载所有翻译"""
    manager = get_language_manager()
    manager.load_translations()
    return True 