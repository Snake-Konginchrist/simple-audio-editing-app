# 简易音频编辑器

[English Documentation](README.en.md) | 中文文档

这是一个简单的桌面应用程序，用于编辑音频文件。应用提供了一个图形用户界面，允许用户执行各种基本的音频编辑操作，如剪切、合并、添加特效等。支持的文件格式包括 MP3、WAV、AAC、OGG、FLAC等。

## 功能特性

- **基本信息查看**：显示音频文件的路径、格式和时长信息
- **剪切和删除**：可以剪取音频的指定部分或删除某一时间段
- **合并音频**：支持多个音频文件的合并，可以调整合并顺序
- **音频效果**：
  - 倒放：将音频从后向前播放
  - 调整音量：增大或减小音频的音量
  - 改变速度：加快或减慢音频播放速度（不改变音调）
  - 淡入/淡出：添加渐入或渐出效果
- **视频提取音频**：
  - 从视频文件中提取音频轨道
  - 灵活的输出选项：
    - 保留原始音频流（无质量损失，适用于兼容格式）
    - 保留原始音频质量（在格式转换时保持原始比特率和采样率）
    - 自定义比特率设置
  - 支持多种视频格式（MP4, AVI, MOV, MKV等）
  - 支持多种音频输出格式（MP3, WAV, AAC, OGG, FLAC, M4A）

## 开始使用

要运行这个程序，你需要在你的系统上安装 Python 和一些依赖库，包括 FFmpeg，用于处理音频文件。

### 先决条件

确保你已安装 Python 3.6+ 和 pip。然后安装项目依赖：

```bash
# 安装基本运行依赖
python install.py

# 或安装开发依赖（包含构建工具）
python install.py --dev
```

这将安装以下依赖：
- pydub：用于音频处理
- ffmpeg-python：用于与 FFmpeg 交互
- 开发模式还会安装：
  - pyinstaller：用于打包应用
  - Pillow：用于图像处理

所有依赖信息都集中在`app_info.json`文件中进行管理。

### 安装 FFmpeg

FFmpeg 是一个必须的组件，用于处理音频和视频文件。以下是各操作系统的安装说明：

#### Windows

1. **下载 FFmpeg**：
   - 访问 [FFmpeg官方下载页面](https://ffmpeg.org/download.html) 或 [FFmpeg Windows 构建](https://www.gyan.dev/ffmpeg/builds/)
   - 下载"essentials"或"full"版本（推荐下载"git-full"版本）

2. **安装 FFmpeg**：
   - 解压下载的文件到一个你喜欢的目录，例如 `C:\FFmpeg`

3. **设置环境变量**：
   - 搜索并打开"系统环境变量"编辑器
   - 编辑 `Path` 环境变量，添加 FFmpeg 的 bin 目录到该变量中，例如 `C:\FFmpeg\bin`
   - 保存更改并重新启动命令提示符

#### macOS

1. **使用 Homebrew 安装（推荐）**：
   ```bash
   # 如果未安装Homebrew，先安装它
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # 然后安装FFmpeg
   brew install ffmpeg
   ```

2. **或使用 MacPorts 安装**：
   ```bash
   sudo port install ffmpeg
   ```

#### Linux

1. **Debian/Ubuntu**：
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

2. **Fedora**：
   ```bash
   sudo dnf install ffmpeg
   ```

3. **CentOS/RHEL**：
   ```bash
   # 启用EPEL和RPM Fusion仓库
   sudo yum install epel-release
   sudo yum localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %rhel).noarch.rpm
   
   # 安装FFmpeg
   sudo yum install ffmpeg
   ```

4. **Arch Linux**：
   ```bash
   sudo pacman -S ffmpeg
   ```

#### 验证安装

在任何操作系统上，打开终端或命令提示符并输入：
```bash
ffmpeg -version
```
如果看到版本信息，则表示安装成功。

### 安装

1. 克隆仓库到本地机器：

```bash
git clone https://gitee.com/Snake-Konginchrist/simple-audio-editing-app.git
cd simple-audio-editing-app
```

2. 运行程序：

```bash
python main.py
```

## 构建可执行文件

本项目提供了一个交互式构建脚本，可以将应用打包为可执行文件：

```bash
python build.py
```

构建脚本提供以下选项：
1. **打包模式**：
   - 单个可执行文件（推荐，体积较大但方便分发）
   - 文件夹（体积较小但需要保持文件结构完整）

2. **控制台窗口**：
   - 隐藏控制台（推荐，正常用户使用）
   - 显示控制台（用于调试，可以查看输出和错误）

3. **FFmpeg打包**：
   - 不打包FFmpeg（推荐，要求用户自行安装FFmpeg）
   - 打包FFmpeg（应用体积会显著增大）

构建完成后，可执行文件将生成在`dist`目录中。

## 使用指南

1. **加载音频文件**：
   - 打开程序后，点击"加载音频文件"按钮选择一个音频文件。
   - 文件信息将显示在基本信息标签页中。

2. **剪切或删除音频片段**：
   - 切换到"剪切/删除"标签页。
   - 输入开始时间和结束时间（格式：分:秒.毫秒，如 01:23.45）。
   - 点击"剪切选定部分"保留该部分，或点击"删除选定部分"删除该部分。

3. **合并多个音频文件**：
   - 切换到"合并音频"标签页。
   - 点击"添加音频文件"选择多个音频文件。
   - 使用"上移"、"下移"和"移除所选"按钮调整文件顺序。
   - 点击"合并选定文件"将文件合并为一个新文件。

4. **添加音频效果**：
   - 切换到"音频效果"标签页。
   - 选择想要的效果并应用：
     - 倒放：点击"倒放音频"按钮。
     - 调整音量：使用滑块设置音量变化值(dB)，点击"应用"。
     - 改变速度：使用滑块设置速度因子，点击"应用"。
     - 淡入/淡出：设置时长并点击对应按钮。

5. **从视频提取音频**：
   - 切换到"视频提取"标签页。
   - 点击"选择视频文件"按钮，选择一个视频文件。
   - 选择输出音频格式（MP3, WAV, AAC等）。
   - 选择音频质量选项：
     - **保留原始音频流**：直接复制原音频（无质量损失，但要求格式兼容）
     - **保留原始音频质量**：使用与原音频相同的比特率和采样率（适用于所有格式转换）
     - **自定义比特率**：手动设置输出音频比特率
   - 点击"提取音频"按钮，然后选择保存位置。
   - 等待提取完成，完成后会显示成功消息。

### 视频音频提取说明

当您需要保持高音质的音频输出时，可以根据需求选择不同的选项：

1. **格式兼容时**（例如MP4视频中的AAC音频提取为AAC或M4A）：
   - 选择"保留原始音频流"可以无损地提取音频

2. **格式不兼容时**（例如将AAC音频转换为MP3）：
   - 选择"保留原始音频质量"可以在转换格式时保持原始的比特率和采样率
   - 系统会自动应用适当的质量设置，确保最佳的音频输出

注意：不同音频格式间的转换总会有一定的质量损失，这是由不同编码算法的本质决定的。选择"保留原始音频质量"可以最大程度地减小这种损失。

## 项目结构

本项目使用模块化设计，代码结构清晰：

```
simple-audio-editing-app/
├── main.py                 # 程序入口点
├── build.py                # 应用打包构建脚本
├── install.py              # 依赖安装脚本
├── app_info.json           # 应用信息与依赖配置
├── icon.ico                # 应用图标
├── LICENSE                 # 许可证文件
├── README.md               # 项目说明文档（中文）
├── README.en.md            # 项目说明文档（英文）
├── src/                    # 源代码目录
│   ├── __init__.py         # 包初始化文件
│   ├── core/               # 核心功能模块
│   │   ├── audio_processor.py  # 音频处理类
│   │   ├── audio_merger.py     # 音频合并功能
│   │   └── ...
│   ├── ui/                 # 用户界面模块
│   │   ├── main_window.py      # 主窗口类
│   │   ├── audio_player.py     # 音频播放器组件
│   │   └── ...
│   └── utils/              # 工具函数模块
│       ├── time_formatter.py   # 时间格式转换工具
│       ├── file_utils.py       # 文件操作工具
│       └── ...
├── build/                  # 构建临时文件（自动生成）
└── dist/                   # 打包后的可执行文件（自动生成）
```

## 技术实现

本项目使用 Python 的 Tkinter 库构建 GUI，使用 pydub 进行音频处理，使用 FFmpeg 进行视频处理。代码结构采用模块化设计，将功能分为三个主要模块：

- **core**：负责音频处理的核心功能，如剪切、合并、添加效果等
- **ui**：负责用户界面的实现，包括主窗口和各个功能模块的界面
- **utils**：提供各种辅助功能，如时间格式转换、文件操作等

## 贡献

欢迎任何形式的贡献。请 Fork 仓库，并提交 Pull Request。

## 版权和许可

本项目在 MIT 许可下发布。详情请见 [LICENSE](LICENSE) 文件。

## 联系方式

- GitHub: [Snake-Konginchrist](https://github.com/Snake-Konginchrist)
- Gitee: [Snake-Konginchrist](https://gitee.com/Snake-Konginchrist)
- Email: developer@skstudio.cn（优先）