from moviepy.editor import VideoFileClip, vfx
from pydub import AudioSegment


def reverse_audio(input_path, output_path):
    # 倒放音频的函数
    audio = AudioSegment.from_file(input_path)  # 加载音频文件
    reversed_audio = audio.reverse()  # 倒放音频
    reversed_audio.export(output_path, format="mp3")  # 导出倒放后的音频


def reverse_video(input_path, output_path):
    # 倒放视频的函数
    video = VideoFileClip(input_path)  # 加载视频文件
    reversed_video = video.fx(vfx.time_mirror)  # 倒放视频
    reversed_video.write_videofile(output_path, codec='libx264')  # 导出倒放后的视频