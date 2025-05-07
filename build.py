#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建脚本 - 用于将简易音频编辑器打包为可执行文件
交互式界面，支持Windows、macOS和Linux系统
"""

import os
import sys
import json
import shutil
import platform
import subprocess
from pathlib import Path

# 从JSON文件加载应用信息
def load_app_info():
    """从app_info.json文件加载应用信息"""
    try:
        with open('app_info.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"错误: 无法加载应用信息 - {e}")
        print("使用默认应用信息...")
        # 默认应用信息
        return {
            "name": "简易音频编辑器",
            "version": "1.0.0",
            "author": "Snake Konginchrist",
            "description": "一个简单的音频编辑桌面应用",
            "main_script": "main.py",
            "icon_file": "icon.ico"
        }

# 加载应用信息
APP_INFO = load_app_info()
APP_NAME = APP_INFO["name"]
APP_VERSION = APP_INFO["version"]
MAIN_SCRIPT = APP_INFO["main_script"]
ICON_FILE = APP_INFO["icon_file"]
AUTHOR = APP_INFO["author"]
DESCRIPTION = APP_INFO["description"]

def clear_screen():
    """清除终端内容"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_header():
    """打印脚本标题"""
    clear_screen()
    print("=" * 60)
    print(f"{APP_NAME} 打包工具 v{APP_VERSION}".center(60))
    print("=" * 60)
    print()

# 检查必要的依赖
def check_dependencies():
    """检查必要的打包依赖是否已安装"""
    print("检查必要依赖...")
    required_packages = ["pyinstaller"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("\n缺少以下必要的依赖包：")
        for package in missing_packages:
            print(f"  - {package}")
        
        install = input("\n是否立即安装这些依赖？(y/n): ").strip().lower()
        if install == 'y':
            try:
                subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, check=True)
                print("✅ 依赖安装成功！")
                return True
            except subprocess.CalledProcessError:
                print("❌ 依赖安装失败，请手动安装后重试。")
                return False
        else:
            print("请安装必要依赖后再运行此脚本。")
            return False
    
    print("✅ 所有必要依赖已安装")
    return True

# 检查FFmpeg是否安装
def check_ffmpeg():
    """检查系统是否已安装FFmpeg"""
    print("检查FFmpeg安装状态...")
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            print("✅ 检测到FFmpeg已安装")
            return True
        else:
            print("❌ 未检测到FFmpeg")
            return False
    except FileNotFoundError:
        print("❌ 未检测到FFmpeg")
        return False

# 清理之前的构建
def clean_build_dirs():
    """清理之前的构建目录"""
    print("清理之前的构建文件...")
    dirs_to_clean = ["build", "dist"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"  - 清理 {dir_name} 目录...")
            shutil.rmtree(dir_name)
    
    # 清理.spec文件
    spec_file = f"{APP_NAME}.spec"
    if os.path.exists(spec_file):
        print(f"  - 删除 {spec_file} 文件...")
        os.remove(spec_file)
    
    print("✅ 清理完成")

# 构建应用
def build_app(one_file=True, console=False, with_ffmpeg=False):
    """
    使用PyInstaller构建应用
    
    参数:
        one_file: 是否打包为单个文件
        console: 是否显示控制台窗口
        with_ffmpeg: 是否打包FFmpeg
    """
    system = platform.system()
    
    # 基本命令参数
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name", APP_NAME,
        "--noconfirm",
    ]
    
    # 如果有图标文件
    if os.path.exists(ICON_FILE):
        cmd.extend(["--icon", ICON_FILE])
    
    # 是否打包为单个文件
    if one_file:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")
    
    # 是否显示控制台
    if not console:
        if system == "Windows":
            cmd.append("--noconsole")
        elif system == "Darwin":  # macOS
            cmd.append("--windowed")
    
    # 添加需要包含的文件和目录
    data_includes = []
    
    # 如果选择打包FFmpeg
    if with_ffmpeg:
        # 在这里需要处理FFmpeg的打包逻辑
        ffmpeg_path = find_ffmpeg()
        if ffmpeg_path:
            ffmpeg_dir = os.path.dirname(ffmpeg_path)
            if system == "Windows":
                ffmpeg_files = ["ffmpeg.exe", "ffprobe.exe"]
                for file in ffmpeg_files:
                    full_path = os.path.join(ffmpeg_dir, file)
                    if os.path.exists(full_path):
                        data_includes.append(f"--add-data={full_path};.")
            else:  # macOS 和 Linux
                data_includes.append(f"--add-data={ffmpeg_path}:.")
    
    # 添加数据文件
    cmd.extend(data_includes)
    
    # 添加主脚本
    cmd.append(MAIN_SCRIPT)
    
    # 执行构建
    print("\n开始构建应用...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ 构建成功！你可以在 dist 目录中找到{'可执行文件' if one_file else '应用目录'}")
        
        # 构建后的路径
        if one_file:
            if system == "Windows":
                build_path = f"dist/{APP_NAME}.exe"
            else:
                build_path = f"dist/{APP_NAME}"
        else:
            build_path = f"dist/{APP_NAME}"
        
        print(f"应用路径: {os.path.abspath(build_path)}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False
    
    return True

# 查找系统中的FFmpeg路径
def find_ffmpeg():
    """查找系统中安装的FFmpeg路径"""
    system = platform.system()
    ffmpeg_cmd = "ffmpeg.exe" if system == "Windows" else "ffmpeg"
    
    try:
        if system == "Windows":
            result = subprocess.run(
                ["where", ffmpeg_cmd], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
        else:  # macOS 和 Linux
            result = subprocess.run(
                ["which", ffmpeg_cmd], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
        
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    return None

# 创建图标
def create_icon_if_missing():
    """如果图标文件不存在，使用默认生成一个简单的图标"""
    if os.path.exists(ICON_FILE):
        return
    
    print("未找到图标文件，尝试创建默认图标...")
    try:
        # 尝试使用PIL创建一个简单的图标
        from PIL import Image, ImageDraw
        
        # 创建一个100x100的图像，蓝色背景
        img = Image.new('RGB', (100, 100), color=(48, 141, 255))
        d = ImageDraw.Draw(img)
        
        # 绘制简单的声波图形
        d.rectangle([(20, 40), (30, 60)], fill=(255, 255, 255))
        d.rectangle([(40, 30), (50, 70)], fill=(255, 255, 255))
        d.rectangle([(60, 20), (70, 80)], fill=(255, 255, 255))
        
        # 保存为ICO文件
        img.save(ICON_FILE)
        print(f"✅ 创建了默认图标文件: {ICON_FILE}")
    except:
        print("⚠️ 无法创建默认图标文件，将使用PyInstaller默认图标")

# 交互式界面
def interactive_build():
    """交互式界面让用户选择构建选项"""
    print_header()
    
    # 显示应用信息
    print(f"应用名称: {APP_NAME}")
    print(f"版本: {APP_VERSION}")
    print(f"作者: {AUTHOR}")
    print(f"描述: {DESCRIPTION}")
    print(f"主脚本: {MAIN_SCRIPT}")
    print(f"图标文件: {ICON_FILE}")
    
    # 检查依赖
    if not check_dependencies():
        input("\n按Enter键退出...")
        return
    
    # 检查FFmpeg
    ffmpeg_installed = check_ffmpeg()
    
    print("\n构建选项配置")
    print("-" * 40)
    
    # 选择打包模式
    print("\n1. 打包模式:")
    print("   [1] 单个可执行文件 (推荐，体积较大但方便分发)")
    print("   [2] 文件夹 (体积较小但需要保持文件结构完整)")
    
    while True:
        mode_choice = input("   选择打包模式 (1/2): ").strip()
        if mode_choice in ['1', '2']:
            break
        print("   无效选择，请重试。")
    
    one_file = mode_choice == '1'
    
    # 是否显示控制台
    print("\n2. 控制台窗口:")
    print("   [1] 隐藏控制台 (推荐，正常用户使用)")
    print("   [2] 显示控制台 (用于调试，可以查看输出和错误)")
    
    while True:
        console_choice = input("   选择控制台选项 (1/2): ").strip()
        if console_choice in ['1', '2']:
            break
        print("   无效选择，请重试。")
    
    console = console_choice == '2'
    
    # 是否打包FFmpeg
    with_ffmpeg = False
    if ffmpeg_installed:
        print("\n3. FFmpeg打包:")
        print("   [1] 不打包FFmpeg (推荐，要求用户自行安装FFmpeg)")
        print("   [2] 打包FFmpeg (应用体积会显著增大)")
        
        while True:
            ffmpeg_choice = input("   选择FFmpeg选项 (1/2): ").strip()
            if ffmpeg_choice in ['1', '2']:
                break
            print("   无效选择，请重试。")
        
        with_ffmpeg = ffmpeg_choice == '2'
    else:
        print("\n❗ 未检测到FFmpeg，无法打包FFmpeg到应用中")
        print("  用户需要自行安装FFmpeg才能使用此应用的完整功能")
    
    # 确认选项
    print("\n已选择的构建选项:")
    print(f"  - {'单个可执行文件' if one_file else '文件夹'}")
    print(f"  - {'显示' if console else '隐藏'}控制台")
    print(f"  - {'打包' if with_ffmpeg else '不打包'}FFmpeg")
    
    confirm = input("\n确认开始构建? (y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消构建。")
        input("\n按Enter键退出...")
        return
    
    # 创建默认图标
    create_icon_if_missing()
    
    # 清理之前的构建
    clean_build_dirs()
    
    # 构建应用
    success = build_app(
        one_file=one_file,
        console=console,
        with_ffmpeg=with_ffmpeg
    )
    
    if success:
        print("\n提示：")
        if not with_ffmpeg:
            print("1. 此应用需要用户系统已安装FFmpeg才能正常工作")
            print("2. 在分发应用时，请确保用户已安装FFmpeg或提供安装说明")
        
        if platform.system() == "Darwin" and one_file:  # macOS单文件模式
            print("3. 在macOS上，单文件模式可能会导致某些权限问题，如遇问题请尝试目录模式")
        
        print("\n祝您使用愉快！")
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    interactive_build() 