from pydub import AudioSegment
import os

class AudioProcessor:
    """
    音频处理类，提供各种音频编辑功能
    """
    
    @staticmethod
    def load_audio(file_path):
        """
        加载音频文件
        
        参数:
            file_path: 音频文件路径
            
        返回:
            AudioSegment对象
        """
        # 根据文件扩展名判断格式
        ext = os.path.splitext(file_path)[1].lower().strip('.')
        return AudioSegment.from_file(file_path, format=ext)
    
    @staticmethod
    def save_audio(audio, output_path):
        """
        保存音频文件
        
        参数:
            audio: AudioSegment对象
            output_path: 输出文件路径
        """
        # 获取文件扩展名作为格式
        ext = os.path.splitext(output_path)[1].lower().strip('.')
        audio.export(output_path, format=ext)
        
    @staticmethod
    def reverse_audio(input_path, output_path):
        """
        倒放音频
        
        参数:
            input_path: 输入文件路径
            output_path: 输出文件路径
        """
        audio = AudioProcessor.load_audio(input_path)
        reversed_audio = audio.reverse()
        AudioProcessor.save_audio(reversed_audio, output_path)
    
    @staticmethod
    def cut_audio(input_path, output_path, start_ms, end_ms):
        """
        剪切音频的指定部分
        
        参数:
            input_path: 输入文件路径
            output_path: 输出文件路径
            start_ms: 开始时间(毫秒)
            end_ms: 结束时间(毫秒)
        """
        audio = AudioProcessor.load_audio(input_path)
        cut_audio = audio[start_ms:end_ms]
        AudioProcessor.save_audio(cut_audio, output_path)
    
    @staticmethod
    def remove_segment(input_path, output_path, start_ms, end_ms):
        """
        从音频中删除一段
        
        参数:
            input_path: 输入文件路径
            output_path: 输出文件路径
            start_ms: 要删除部分的开始时间(毫秒)
            end_ms: 要删除部分的结束时间(毫秒)
        """
        audio = AudioProcessor.load_audio(input_path)
        # 保留删除部分前后的音频并合并
        first_part = audio[:start_ms]
        second_part = audio[end_ms:]
        result_audio = first_part + second_part
        AudioProcessor.save_audio(result_audio, output_path)
    
    @staticmethod
    def merge_audios(input_paths, output_path):
        """
        合并多个音频文件
        
        参数:
            input_paths: 输入文件路径列表
            output_path: 输出文件路径
        """
        if not input_paths:
            return
            
        # 加载第一个音频作为基础
        merged_audio = AudioProcessor.load_audio(input_paths[0])
        
        # 依次合并其他音频
        for path in input_paths[1:]:
            next_audio = AudioProcessor.load_audio(path)
            merged_audio += next_audio
            
        AudioProcessor.save_audio(merged_audio, output_path)
    
    @staticmethod
    def adjust_volume(input_path, output_path, volume_db):
        """
        调整音频音量
        
        参数:
            input_path: 输入文件路径
            output_path: 输出文件路径
            volume_db: 音量调整值(分贝)，正值增加音量，负值降低音量
        """
        audio = AudioProcessor.load_audio(input_path)
        adjusted_audio = audio + volume_db  # pydub中可以直接用+/-来调整分贝
        AudioProcessor.save_audio(adjusted_audio, output_path)
    
    @staticmethod
    def change_speed(input_path, output_path, speed_factor):
        """
        改变音频速度（不改变音调）
        
        参数:
            input_path: 输入文件路径
            output_path: 输出文件路径
            speed_factor: 速度因子，>1加速，<1减速
        """
        audio = AudioProcessor.load_audio(input_path)
        # 通过修改采样率来改变速度
        adjusted_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * speed_factor)
        }).set_frame_rate(audio.frame_rate)
        AudioProcessor.save_audio(adjusted_audio, output_path)
    
    @staticmethod
    def fade_in(input_path, output_path, fade_ms):
        """
        添加淡入效果
        
        参数:
            input_path: 输入文件路径
            output_path: 输出文件路径
            fade_ms: 淡入时长(毫秒)
        """
        audio = AudioProcessor.load_audio(input_path)
        faded_audio = audio.fade_in(fade_ms)
        AudioProcessor.save_audio(faded_audio, output_path)
    
    @staticmethod
    def fade_out(input_path, output_path, fade_ms):
        """
        添加淡出效果
        
        参数:
            input_path: 输入文件路径
            output_path: 输出文件路径
            fade_ms: 淡出时长(毫秒)
        """
        audio = AudioProcessor.load_audio(input_path)
        faded_audio = audio.fade_out(fade_ms)
        AudioProcessor.save_audio(faded_audio, output_path) 