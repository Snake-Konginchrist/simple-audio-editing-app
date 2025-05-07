# Simple Audio Editor

A desktop application for basic audio editing. The app provides a graphical user interface that allows users to perform various basic audio editing operations, such as cutting, merging, adding effects, etc. Supported file formats include MP3, WAV, AAC, OGG, FLAC, and more.

## Features

- **Basic Information View**: Display the audio file's path, format, and duration information
- **Cut and Delete**: Cut or delete specific portions of audio files
- **Merge Audio**: Combine multiple audio files with adjustable order
- **Audio Effects**:
  - Reverse: Play audio backwards
  - Adjust Volume: Increase or decrease audio volume
  - Change Speed: Speed up or slow down audio playback (without changing pitch)
  - Fade In/Out: Add gradual volume increase or decrease effects
- **Extract Audio from Video**:
  - Extract audio tracks from video files
  - Flexible output options:
    - Keep original audio stream (no quality loss, for compatible formats)
    - Maintain original audio quality (preserve original bitrate and sample rate during format conversion)
    - Custom bitrate settings
  - Support for various video formats (MP4, AVI, MOV, MKV, etc.)
  - Support for multiple audio output formats (MP3, WAV, AAC, OGG, FLAC, M4A)
- **Multilingual Support**:
  - Built-in Chinese and English interfaces
  - Language can be switched from the File menu
  - Complete translations for all UI elements and messages

## Getting Started

To run this program, you need to have Python and some dependencies installed on your system, including FFmpeg for processing audio files.

### Prerequisites

Ensure you have Python 3.6+ and pip installed. Then install the project dependencies:

```bash
# Install basic runtime dependencies
python install.py

# Or install development dependencies (including build tools)
python install.py --dev
```

This will install the following dependencies:
- pydub: for audio processing
- ffmpeg-python: for interacting with FFmpeg
- In development mode, it will also install:
  - pyinstaller: for packaging the application
  - Pillow: for image processing

All dependency information is centrally managed in the `app_info.json` file.

### Installing FFmpeg

FFmpeg is a required component for processing audio and video files. Here are installation instructions for various operating systems:

#### Windows

1. **Download FFmpeg**:
   - Visit the [FFmpeg official download page](https://ffmpeg.org/download.html) or [FFmpeg Windows builds](https://www.gyan.dev/ffmpeg/builds/)
   - Download the "essentials" or "full" version (the "git-full" version is recommended)

2. **Install FFmpeg**:
   - Extract the downloaded file to a directory of your choice, such as `C:\FFmpeg`

3. **Set Environment Variables**:
   - Search for and open the "Edit System Environment Variables" editor
   - Edit the `Path` environment variable, adding the FFmpeg bin directory to it, e.g., `C:\FFmpeg\bin`
   - Save changes and restart the command prompt

#### macOS

1. **Install using Homebrew (recommended)**:
   ```bash
   # If Homebrew is not installed, install it first
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Then install FFmpeg
   brew install ffmpeg
   ```

2. **Or install using MacPorts**:
   ```bash
   sudo port install ffmpeg
   ```

#### Linux

1. **Debian/Ubuntu**:
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

2. **Fedora**:
   ```bash
   sudo dnf install ffmpeg
   ```

3. **CentOS/RHEL**:
   ```bash
   # Enable EPEL and RPM Fusion repositories
   sudo yum install epel-release
   sudo yum localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %rhel).noarch.rpm
   
   # Install FFmpeg
   sudo yum install ffmpeg
   ```

4. **Arch Linux**:
   ```bash
   sudo pacman -S ffmpeg
   ```

#### Verify Installation

On any operating system, open a terminal or command prompt and type:
```bash
ffmpeg -version
```
If you see version information, the installation was successful.

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://gitee.com/Snake-Konginchrist/simple-audio-editing-app.git
cd simple-audio-editing-app
```

2. Run the program:

```bash
python main.py
```

## Building Executable Files

This project provides an interactive build script to package the application as an executable:

```bash
python build.py
```

The build script offers the following options:
1. **Packaging Mode**:
   - Single executable file (recommended, larger size but easier to distribute)
   - Folder (smaller size but requires maintaining the file structure)

2. **Console Window**:
   - Hide console (recommended for normal users)
   - Show console (for debugging, allows viewing output and errors)

3. **FFmpeg Packaging**:
   - Don't package FFmpeg (recommended, requires users to install FFmpeg separately)
   - Package FFmpeg (significantly increases application size)

After building, the executable will be generated in the `dist` directory.

### Packaging Mode Features

- **Single-file Mode**: Packages all dependencies and resources into a single executable file, convenient for distribution but larger in size.
- **Folder Mode**: Generates a folder containing multiple files, smaller in size but requires maintaining the file structure for distribution. Folder mode also generates log files (located in the logs directory) for debugging and troubleshooting.

## Usage Guide

1. **Load Audio File**:
   - After opening the program, click the "Load Audio File" button to select an audio file.
   - File information will be displayed in the Basic Information tab.

2. **Cut or Delete Audio Segments**:
   - Switch to the "Cut/Delete" tab.
   - Enter the start and end times (format: minutes:seconds.milliseconds, e.g., 01:23.45).
   - Click "Cut Selected Portion" to keep that part, or "Delete Selected Portion" to remove it.

3. **Merge Multiple Audio Files**:
   - Switch to the "Merge Audio" tab.
   - Click "Add Audio Files" to select multiple audio files.
   - Use the "Move Up", "Move Down", and "Remove Selected" buttons to adjust the file order.
   - Click "Merge Selected Files" to combine the files into a new file.

4. **Add Audio Effects**:
   - Switch to the "Audio Effects" tab.
   - Select the desired effect and apply:
     - Reverse: Click the "Reverse Audio" button.
     - Adjust Volume: Use the slider to set the volume change value (dB), then click "Apply".
     - Change Speed: Use the slider to set the speed factor, then click "Apply".
     - Fade In/Out: Set the duration and click the corresponding button.

5. **Extract Audio from Video**:
   - Switch to the "Video Extract" tab.
   - Click the "Select Video File" button to choose a video file.
   - Select the output audio format (MP3, WAV, AAC, etc.).
   - Choose an audio quality option:
     - **Keep Original Audio Stream**: Direct copy of the original audio (no quality loss, but requires format compatibility)
     - **Maintain Original Audio Quality**: Use the same bitrate and sample rate as the original audio (suitable for all format conversions)
     - **Custom Bitrate**: Manually set the output audio bitrate
   - Click the "Extract Audio" button, then select a save location.
   - Wait for the extraction to complete; a success message will be displayed upon completion.

6. **Switch Language**:
   - Click the "File" menu.
   - Select "Language" from the dropdown menu.
   - Choose your preferred language (简体中文 or English) from the submenu.
   - The program will ask if you want to restart the application immediately to apply the new language setting.

### Video Audio Extraction Notes

When you need high-quality audio output, you can choose different options based on your needs:

1. **For compatible formats** (e.g., extracting AAC audio from MP4 video to AAC or M4A):
   - Choose "Keep Original Audio Stream" for lossless audio extraction

2. **For incompatible formats** (e.g., converting AAC audio to MP3):
   - Choose "Maintain Original Audio Quality" to preserve the original bitrate and sample rate during format conversion
   - The system will automatically apply appropriate quality settings to ensure the best audio output

Note: There will always be some quality loss when converting between different audio formats due to the nature of different encoding algorithms. Choosing "Maintain Original Audio Quality" can minimize this loss as much as possible.

## Project Structure

This project uses a modular design with a clear code structure:

```
simple-audio-editing-app/
├── main.py                 # Program entry point
├── build.py                # Application packaging script
├── install.py              # Dependency installation script
├── app_info.json           # Application information and dependency configuration
├── icon.ico                # Application icon
├── LICENSE                 # License file
├── README.md               # Project documentation (Chinese)
├── README.en.md            # Project documentation (English)
├── src/                    # Source code directory
│   ├── __init__.py         # Package initialization file
│   ├── core/               # Core functionality module
│   │   ├── audio_processor.py  # Audio processing class
│   │   ├── audio_merger.py     # Audio merging functionality
│   │   └── ...
│   ├── ui/                 # User interface module
│   │   ├── main_window.py      # Main window class
│   │   ├── audio_player.py     # Audio player component
│   │   └── ...
│   ├── locales/            # Multilingual support
│   │   ├── zh_CN.json          # Simplified Chinese translation
│   │   ├── en_US.json          # English translation
│   │   └── ...
│   └── utils/              # Utility functions module
│       ├── time_formatter.py   # Time format conversion tool
│       ├── file_utils.py       # File operation tools
│       ├── language.py         # Language support utility
│       └── ...
├── build/                  # Build temporary files (auto-generated)
└── dist/                   # Packaged executables (auto-generated)
```

## Technical Implementation

This project uses Python's Tkinter library to build the GUI, pydub for audio processing, and FFmpeg for video processing. The code structure adopts a modular design, dividing functionality into three main modules:

- **core**: Responsible for core audio processing functions such as cutting, merging, adding effects, etc.
- **ui**: Responsible for implementing the user interface, including the main window and the interfaces for various functional modules
- **utils**: Provides various auxiliary functions, such as time format conversion, file operations, etc.
- **locales**: Provides multilingual support, containing translation files for different languages

## Contributing

Contributions of any form are welcome. Please fork the repository and submit a Pull Request.

## Copyright and License

This project is released under the MIT license. See the [LICENSE](LICENSE) file for details.

## Contact Information

- GitHub: [Snake-Konginchrist](https://github.com/Snake-Konginchrist)
- Gitee: [Snake-Konginchrist](https://gitee.com/Snake-Konginchrist)
- Email: developer@skstudio.cn (preferred) 