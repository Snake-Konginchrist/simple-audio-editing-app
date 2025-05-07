#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语言工具模块 - 提供多语言支持
从JSON文件读取界面文本资源
"""

import os
import json
import logging
from pathlib import Path

# 支持的语言
LANGUAGE_CHINESE = "zh_CN"
LANGUAGE_ENGLISH = "en_US"

# 默认语言
DEFAULT_LANGUAGE = LANGUAGE_CHINESE

# 翻译文件目录
LOCALE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "locales")

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
        
        for lang_code in SUPPORTED_LANGUAGES.keys():
            try:
                # 构建翻译文件路径
                translation_file = os.path.join(LOCALE_DIR, f"{lang_code}.json")
                
                # 读取翻译文件
                with open(translation_file, 'r', encoding='utf-8') as file:
                    self.translations[lang_code] = json.load(file)
                logging.info(f"已加载{lang_code}语言文件")
            except Exception as e:
                logging.error(f"加载{lang_code}语言文件失败: {e}")
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