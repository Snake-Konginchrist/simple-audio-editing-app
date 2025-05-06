from setuptools import setup, find_packages

setup(
    name="简易音频编辑器",
    version="1.0.0",
    description="一个简单的桌面应用程序，用于编辑音频文件",
    author="Snake-Konginchrist",
    author_email="developer@skstudio.cn",
    packages=find_packages(),
    install_requires=[
        "pydub>=0.25.1",
        "ffmpeg-python>=0.2.0",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "audio-editor=main:main",
        ],
    },
) 