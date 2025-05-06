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
        
    @staticmethod
    def preview_audio(audio_data_or_path, start_ms=0, duration_ms=None):
        """
        预览音频片段
        
        参数:
            audio_data_or_path: AudioSegment对象或音频文件路径
            start_ms: 开始时间(毫秒)
            duration_ms: 持续时间(毫秒)，None表示播放到结束
            
        返回:
            None
        """
        import tempfile
        import os
        import platform
        import subprocess
        
        # 如果传入的是路径而不是AudioSegment对象
        if isinstance(audio_data_or_path, str):
            audio = AudioProcessor.load_audio(audio_data_or_path)
        else:
            audio = audio_data_or_path
            
        # 如果指定了开始时间和持续时间，则截取相应片段
        if duration_ms:
            audio = audio[start_ms:start_ms + duration_ms]
        elif start_ms > 0:
            audio = audio[start_ms:]
            
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_path = temp_file.name
            
        # 导出到临时文件
        audio.export(temp_path, format="wav")
        
        # 根据操作系统使用不同的命令播放音频
        system = platform.system()
        try:
            if system == 'Darwin':  # macOS
                subprocess.Popen(['afplay', temp_path])
            elif system == 'Windows':
                os.startfile(temp_path)
            elif system == 'Linux':
                subprocess.Popen(['aplay', temp_path])
        except Exception as e:
            print(f"预览音频时出错: {e}")
            
        # 注意：临时文件会在系统重启后自动清理，或者可以实现一个定时清理机制
            
    @staticmethod
    def preview_operation(input_paths, operation_func, *args, **kwargs):
        """
        预览任何音频操作的结果
        
        参数:
            input_paths: 输入音频文件路径或路径列表
            operation_func: 要预览的音频处理函数
            *args, **kwargs: 传递给操作函数的参数
        """
        # 创建临时音频用于预览
        audio_result = None
        
        # 根据不同操作类型进行处理
        if operation_func == AudioProcessor.cut_audio:
            # 剪切音频预览
            audio = AudioProcessor.load_audio(input_paths)
            start_ms = args[0]
            end_ms = args[1]
            audio_result = audio[start_ms:end_ms]
            
        elif operation_func == AudioProcessor.remove_segment:
            # 删除片段预览
            audio = AudioProcessor.load_audio(input_paths)
            start_ms = args[0]
            end_ms = args[1]
            first_part = audio[:start_ms]
            second_part = audio[end_ms:]
            audio_result = first_part + second_part
            
        elif operation_func == AudioProcessor.merge_audios or operation_func == AudioProcessor.merge_audios_with_gaps:
            # 合并音频预览
            if operation_func == AudioProcessor.merge_audios:
                # 简单合并
                merged_audio = AudioProcessor.load_audio(input_paths[0])
                for path in input_paths[1:]:
                    next_audio = AudioProcessor.load_audio(path)
                    merged_audio += next_audio
                audio_result = merged_audio
                
            else:
                # 带间隙合并
                gaps_ms = args[0] if args else None
                
                if not input_paths:
                    return
                    
                # 加载第一个音频
                audio_result = AudioProcessor.load_audio(input_paths[0])
                
                # 依次合并其他音频，添加间隙
                for i, path in enumerate(input_paths[1:], 1):
                    # 添加间隙
                    if gaps_ms and i-1 < len(gaps_ms) and gaps_ms[i-1] > 0:
                        silence = AudioSegment.silent(duration=gaps_ms[i-1])
                        audio_result += silence
                        
                    # 添加下一个音频
                    next_audio = AudioProcessor.load_audio(path)
                    audio_result += next_audio
                    
        elif operation_func == AudioProcessor.add_silence:
            # 添加静音预览
            audio = AudioProcessor.load_audio(input_paths)
            position_ms = args[0]
            duration_ms = args[1]
            
            # 分割音频
            first_part = audio[:position_ms]
            second_part = audio[position_ms:]
            
            # 创建静音段
            silence = AudioSegment.silent(duration=duration_ms)
            
            # 合并三段
            audio_result = first_part + silence + second_part
            
        elif operation_func == AudioProcessor.reverse_audio:
            # 倒放预览
            audio = AudioProcessor.load_audio(input_paths)
            audio_result = audio.reverse()
            
        elif operation_func == AudioProcessor.adjust_volume:
            # 调整音量预览
            audio = AudioProcessor.load_audio(input_paths)
            volume_db = args[0]
            audio_result = audio + volume_db
            
        elif operation_func == AudioProcessor.change_speed:
            # 改变速度预览
            audio = AudioProcessor.load_audio(input_paths)
            speed_factor = args[0]
            audio_result = audio._spawn(audio.raw_data, overrides={
                "frame_rate": int(audio.frame_rate * speed_factor)
            }).set_frame_rate(audio.frame_rate)
            
        elif operation_func == AudioProcessor.fade_in:
            # 淡入预览
            audio = AudioProcessor.load_audio(input_paths)
            fade_ms = args[0]
            audio_result = audio.fade_in(fade_ms)
            
        elif operation_func == AudioProcessor.fade_out:
            # 淡出预览
            audio = AudioProcessor.load_audio(input_paths)
            fade_ms = args[0]
            audio_result = audio.fade_out(fade_ms)
        
        # 预览结果
        if audio_result:
            AudioProcessor.preview_audio(audio_result)

    @staticmethod
    def merge_audios_with_gaps(input_paths, output_path, gaps_ms=None):
        """
        合并多个音频文件，可在文件之间添加指定长度的间隙
        
        参数:
            input_paths: 输入文件路径列表
            output_path: 输出文件路径
            gaps_ms: 间隙长度列表(毫秒)，None表示无间隙
                    例如：[1000, 2000] 表示在第一个和第二个音频之间添加1秒，
                    在第二个和第三个音频之间添加2秒的间隙
        """
        if not input_paths:
            return
            
        # 加载第一个音频作为基础
        merged_audio = AudioProcessor.load_audio(input_paths[0])
        
        # 依次合并其他音频，添加间隙
        for i, path in enumerate(input_paths[1:], 1):
            # 如果指定了间隙并且索引有效
            if gaps_ms and i-1 < len(gaps_ms) and gaps_ms[i-1] > 0:
                # 创建指定长度的静音
                silence = AudioSegment.silent(duration=gaps_ms[i-1])
                merged_audio += silence
                
            # 添加下一个音频
            next_audio = AudioProcessor.load_audio(path)
            merged_audio += next_audio
            
        AudioProcessor.save_audio(merged_audio, output_path)

    @staticmethod
    def add_silence(input_path, output_path, position_ms, duration_ms):
        """
        在音频的指定位置添加静音
        
        参数:
            input_path: 输入文件路径
            output_path: 输出文件路径
            position_ms: 插入位置(毫秒)，0表示在开头
            duration_ms: 静音持续时间(毫秒)
        """
        audio = AudioProcessor.load_audio(input_path)
        
        # 限制位置在音频范围内
        position_ms = max(0, min(len(audio), position_ms))
        
        # 分割音频
        first_part = audio[:position_ms]
        second_part = audio[position_ms:]
        
        # 创建静音段
        silence = AudioSegment.silent(duration=duration_ms)
        
        # 合并三段
        result_audio = first_part + silence + second_part
        
        AudioProcessor.save_audio(result_audio, output_path) 