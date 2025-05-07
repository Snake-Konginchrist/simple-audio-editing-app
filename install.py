#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装脚本 - 用于安装简易音频编辑器的依赖
从app_info.json读取依赖信息并安装
"""

import json
import sys
import subprocess
import os

def load_app_info():
    """从app_info.json文件加载应用信息"""
    try:
        with open('app_info.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"错误: 无法加载应用信息 - {e}")
        sys.exit(1)

def install_dependencies(development=False):
    """安装应用依赖"""
    app_info = load_app_info()
    
    # 基本依赖
    dependencies = app_info["dependencies"]
    
    # 如果是开发模式，添加构建依赖
    if development:
        dependencies.extend(app_info["build_dependencies"])
    
    print(f"正在安装{'开发模式' if development else '基本'}依赖...")
    for dep in dependencies:
        print(f"  - {dep}")
    
    try:
        # 使用pip安装依赖
        cmd = [sys.executable, "-m", "pip", "install"] + dependencies
        subprocess.run(cmd, check=True)
        print("✅ 依赖安装成功！")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        sys.exit(1)

def main():
    """脚本入口点"""
    import argparse
    parser = argparse.ArgumentParser(description='安装简易音频编辑器依赖')
    parser.add_argument('--dev', action='store_true', help='安装开发依赖（包含构建工具）')
    args = parser.parse_args()
    
    install_dependencies(development=args.dev)
    
    # 提示如何安装FFmpeg
    print("\n注意: 此应用需要FFmpeg才能正常工作。")
    print("请参考README.md文件中的说明安装FFmpeg。")

if __name__ == "__main__":
    main() 