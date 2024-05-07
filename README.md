# Audio-Video Reverse App

这是一个简单的桌面应用程序，用于倒放音频和视频文件。应用提供了一个图形用户界面，允许用户上传文件，选择保存的位置，并执行倒放操作。支持的文件格式包括 MP3、WAV、MP4 和 AVI。

## 开始使用

要运行这个程序，你需要在你的系统上安装 Python 和一些依赖库，包括 FFmpeg，用于处理音视频文件。

### 先决条件

确保你已安装 Python 和 pip。此外，你还需要安装以下库：

```bash
pip install moviepy pydub tkinter
```

### 安装 FFmpeg

FFmpeg 是一个必须的组件，用于处理音频和视频文件。按照以下步骤安装和配置 FFmpeg：

1. **下载 FFmpeg**：
   - 访问 [FFmpeg官方下载页面](https://ffmpeg.org/download.html)。
   - 根据你的操作系统下载适合的版本。

2. **安装 FFmpeg**：
   - 解压下载的文件到一个你喜欢的目录，例如 `C:\FFmpeg`。

3. **设置环境变量**：
   - 在 Windows 上，搜索并打开“系统环境变量”编辑器。
   - 编辑 `Path` 环境变量，添加 FFmpeg 的 bin 目录到该变量中，例如 `C:\FFmpeg\bin`。
   - 保存更改并重新启动你的开发环境或计算机。

4. **验证 FFmpeg 安装**：
   - 打开命令行，输入 `ffmpeg -version`，如果看到版本信息，则表示安装成功。

### 安装

1. 克隆仓库到本地机器：

```bash
git clone https://gitee.com/Snake-Konginchrist/audio-video-reverse-app.git
cd audio-video-reverse-app
```

2. 运行程序：

```bash
python main.py
```

## 功能

- **上传音视频文件**：选择你想要倒放的音频或视频文件。
- **倒放处理**：程序将处理文件并将倒放后的结果保存到你选择的位置。
- **支持格式**：MP3, WAV, MP4, AVI。

## 构建

本项目使用 Python 的 Tkinter 库构建 GUI，使用 moviepy 和 pydub 进行音视频处理。

## 贡献

欢迎任何形式的贡献。请 Fork 仓库，并提交 Pull Request。

## 版权和许可

本项目在 MIT 许可下发布。详情请见 [LICENSE](LICENSE) 文件。

## 联系方式
- GitHub: [Snake-Konginchrist](https://github.com/Snake-Konginchrist)
- Gitee: [Snake-Konginchrist](https://gitee.com/Snake-Konginchrist)
- Email: developer@skstudio.cn（优先）