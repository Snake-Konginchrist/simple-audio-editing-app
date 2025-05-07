#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置工具模块 - 用于保存和加载用户配置
支持保存用户偏好设置，如语言选择
"""

import os
import json
import logging
from pathlib import Path

# 配置文件路径
CONFIG_DIR = os.path.join(str(Path.home()), ".audio_editor")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# 默认配置
DEFAULT_CONFIG = {
    "language": "zh_CN",  # 默认语言为中文
    "recent_files": [],  # 最近打开的文件
    "theme": "default",  # 界面主题
    "default_output_dir": "",  # 默认输出目录
    "default_audio_format": "mp3"  # 默认音频格式
}


def ensure_config_dir():
    """确保配置目录存在"""
    if not os.path.exists(CONFIG_DIR):
        try:
            os.makedirs(CONFIG_DIR)
            return True
        except Exception as e:
            logging.error(f"创建配置目录失败: {e}")
            return False
    return True


def load_config():
    """加载用户配置，如果不存在则创建默认配置"""
    if not ensure_config_dir():
        return DEFAULT_CONFIG.copy()
    
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 确保配置包含所有默认项
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        else:
            # 配置文件不存在，创建默认配置
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    except Exception as e:
        logging.error(f"加载配置失败: {e}")
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """保存用户配置"""
    if not ensure_config_dir():
        return False
    
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logging.error(f"保存配置失败: {e}")
        return False


# 缓存的配置
_config_cache = None

def get_config():
    """获取配置，使用缓存减少文件读取"""
    global _config_cache
    if _config_cache is None:
        _config_cache = load_config()
    return _config_cache


def get_config_value(key, default=None):
    """获取指定配置项的值"""
    config = get_config()
    return config.get(key, default)


def set_config_value(key, value):
    """设置指定配置项的值"""
    global _config_cache
    config = get_config()
    config[key] = value
    _config_cache = config  # 更新缓存
    return save_config(config)


def get_language():
    """获取当前语言设置"""
    return get_config_value("language", DEFAULT_CONFIG["language"])


def set_language(language):
    """设置当前语言"""
    return set_config_value("language", language)


def add_recent_file(file_path):
    """添加文件到最近打开文件列表"""
    file_path = os.path.abspath(file_path)
    config = get_config()
    recent_files = config.get("recent_files", [])
    
    # 如果文件已在列表中，先移除
    if file_path in recent_files:
        recent_files.remove(file_path)
    
    # 将文件添加到列表开头
    recent_files.insert(0, file_path)
    
    # 保留最近的10个文件
    config["recent_files"] = recent_files[:10]
    
    return save_config(config)


def get_recent_files():
    """获取最近打开的文件列表"""
    return get_config_value("recent_files", []) 