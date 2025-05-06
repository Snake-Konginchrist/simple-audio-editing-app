import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
import math

from src.utils import (
    load_multiple_audio_files, 
    save_audio_file, 
    show_error, 
    show_info,
    format_time,
    get_audio_duration
)
from src.core import AudioProcessor
from .base_tab import BaseTab

class MergeTab(BaseTab):
    """
    合并音频选项卡
    """
    def __init__(self, parent, app):
        self.audio_files = []
        self.audio_durations = []  # 存储每个音频文件的时长
        self.audio_blocks = []     # 存储音频块的引用
        self.gap_blocks = []       # 存储间隙块的引用
        self.gaps_ms = []          # 存储间隙时间(毫秒)
        self.timeline_scale = 50   # 时间轴比例 (像素/秒)
        super().__init__(parent, app)
    
    def create_widgets(self):
        # 合并部分
        merge_frame = ttk.LabelFrame(self.frame, text="合并多个音频文件", padding="10")
        merge_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 按钮
        button_frame = ttk.Frame(merge_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        add_button = ttk.Button(button_frame, text="添加音频文件", command=self.add_files)
        add_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="清空列表", command=self.clear_files)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        preview_button = ttk.Button(button_frame, text="预览合并效果", command=self.preview_merge)
        preview_button.pack(side=tk.LEFT, padx=5)
        
        merge_button = ttk.Button(button_frame, text="合并选定文件", command=self.merge_files)
        merge_button.pack(side=tk.LEFT, padx=5)
        
        # 音频文件列表框架
        list_frame = ttk.LabelFrame(merge_frame, text="音频文件列表", padding="10")
        list_frame.pack(fill=tk.X, pady=10)
        
        # 创建列表框架和滚动条
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set, selectmode=tk.EXTENDED)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        # 文件列表下方的操作按钮
        action_frame = ttk.Frame(list_frame)
        action_frame.pack(fill=tk.X, pady=5)
        
        move_up_button = ttk.Button(action_frame, text="上移", command=self.move_up)
        move_up_button.pack(side=tk.LEFT, padx=5)
        
        move_down_button = ttk.Button(action_frame, text="下移", command=self.move_down)
        move_down_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = ttk.Button(action_frame, text="移除所选", command=self.remove_selected)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # 时间轴可视化区域
        self.create_timeline_visualization(merge_frame)
    
    def create_timeline_visualization(self, parent_frame):
        """创建时间轴可视化界面"""
        timeline_frame = ttk.LabelFrame(parent_frame, text="音频时间轴与间隙可视化", padding="10")
        timeline_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 工具栏
        tools_frame = ttk.Frame(timeline_frame)
        tools_frame.pack(fill=tk.X, pady=5)
        
        # 缩放控制
        ttk.Label(tools_frame, text="缩放:").pack(side=tk.LEFT, padx=(0, 5))
        zoom_out = ttk.Button(tools_frame, text="-", width=2, command=self.zoom_out_timeline)
        zoom_out.pack(side=tk.LEFT)
        zoom_in = ttk.Button(tools_frame, text="+", width=2, command=self.zoom_in_timeline)
        zoom_in.pack(side=tk.LEFT, padx=(2, 10))
        
        # 添加间隙按钮
        add_gap_button = ttk.Button(tools_frame, text="在选定位置添加空白", command=self.add_gap_at_selection)
        add_gap_button.pack(side=tk.LEFT, padx=5)
        
        # 间隙持续时间输入
        ttk.Label(tools_frame, text="空白时长(秒):").pack(side=tk.LEFT, padx=(10, 0))
        self.gap_duration_var = tk.DoubleVar(value=1.0)
        gap_spin = ttk.Spinbox(tools_frame, from_=0.1, to=60, increment=0.1, textvariable=self.gap_duration_var, width=4)
        gap_spin.pack(side=tk.LEFT, padx=5)
        
        # 滚动条容器
        canvas_container = ttk.Frame(timeline_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 垂直滚动条
        v_scrollbar = ttk.Scrollbar(canvas_container)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 水平滚动条
        h_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建画布
        self.timeline_canvas = tk.Canvas(canvas_container, 
                                 height=150, 
                                 bg="#f0f0f0", 
                                 yscrollcommand=v_scrollbar.set,
                                 xscrollcommand=h_scrollbar.set)
        self.timeline_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 配置滚动条
        v_scrollbar.config(command=self.timeline_canvas.yview)
        h_scrollbar.config(command=self.timeline_canvas.xview)
        
        # 创建时间标尺
        self.ruler_canvas = tk.Canvas(timeline_frame, height=20, bg="#e0e0e0")
        self.ruler_canvas.pack(fill=tk.X, pady=(0, 5))
        
        # 绑定鼠标事件
        self.timeline_canvas.bind("<ButtonPress-1>", self.on_timeline_click)
        self.timeline_canvas.bind("<B1-Motion>", self.on_timeline_drag)
        self.timeline_canvas.bind("<ButtonRelease-1>", self.on_timeline_release)
        
        # 初始选中的项
        self.selected_item = None
        self.drag_start_x = 0
        self.initial_gap_width = 0
    
    def zoom_in_timeline(self):
        """放大时间轴"""
        if self.timeline_scale < 200:  # 限制最大缩放
            self.timeline_scale += 10
            self.update_timeline()
    
    def zoom_out_timeline(self):
        """缩小时间轴"""
        if self.timeline_scale > 20:  # 限制最小缩放
            self.timeline_scale -= 10
            self.update_timeline()
    
    def on_timeline_click(self, event):
        """时间轴点击事件"""
        # 获取点击的项
        item = self.timeline_canvas.find_closest(event.x, event.y)
        if item:
            tags = self.timeline_canvas.gettags(item)
            if "gap" in tags:
                self.selected_item = item
                self.drag_start_x = event.x
                # 获取当前间隙宽度
                x1, _, x2, _ = self.timeline_canvas.coords(item)
                self.initial_gap_width = x2 - x1
                # 高亮显示选中的间隙
                self.timeline_canvas.itemconfig(item, fill="#a0c4ff")
            elif "audio" in tags:
                # 获取音频块的索引
                for i, block in enumerate(self.audio_blocks):
                    if block == item[0]:
                        # 选中对应的列表项
                        self.files_listbox.selection_clear(0, tk.END)
                        self.files_listbox.selection_set(i)
                        self.files_listbox.see(i)
                        break
    
    def on_timeline_drag(self, event):
        """时间轴拖拽事件"""
        if self.selected_item:
            # 计算拖拽距离
            dx = event.x - self.drag_start_x
            
            # 获取对应的间隙索引
            gap_index = self.gap_blocks.index(self.selected_item)
            
            # 计算新的宽度，确保最小宽度
            new_width = max(10, self.initial_gap_width + dx)
            
            # 更新间隙宽度
            x1, y1, _, y2 = self.timeline_canvas.coords(self.selected_item)
            self.timeline_canvas.coords(self.selected_item, x1, y1, x1 + new_width, y2)
            
            # 更新后续音频块和间隙的位置
            self.update_blocks_after(gap_index, new_width - self.initial_gap_width)
            
            # 更新间隙时间
            self.gaps_ms[gap_index] = int(new_width / self.timeline_scale * 1000)
            
            # 更新时间标签
            self.update_gap_label(gap_index)
    
    def on_timeline_release(self, event):
        """时间轴释放事件"""
        if self.selected_item:
            # 重置选中状态
            self.timeline_canvas.itemconfig(self.selected_item, fill="#e0e0e0")
            self.selected_item = None
    
    def update_blocks_after(self, gap_index, dx):
        """更新指定间隙后的所有块位置"""
        # 获取所有需要更新的块
        for i in range(gap_index + 1, len(self.audio_blocks)):
            # 移动音频块
            self.timeline_canvas.move(self.audio_blocks[i], dx, 0)
            
            # 移动对应的标签
            self.timeline_canvas.move(f"audio_label_{i}", dx, 0)
            
            # 如果有间隙，也移动间隙
            if i < len(self.gap_blocks):
                self.timeline_canvas.move(self.gap_blocks[i], dx, 0)
                self.timeline_canvas.move(f"gap_label_{i}", dx, 0)
        
        # 更新画布滚动区域
        self.update_canvas_scroll_region()
    
    def update_canvas_scroll_region(self):
        """更新画布滚动区域"""
        # 计算所有内容的总宽度
        if not self.audio_blocks:
            total_width = 100
        else:
            # 获取最后一个音频块的右边界
            last_audio = self.audio_blocks[-1]
            x1, _, x2, _ = self.timeline_canvas.coords(last_audio)
            total_width = x2 + 50  # 添加一些额外空间
        
        self.timeline_canvas.config(scrollregion=(0, 0, total_width, 150))
        self.ruler_canvas.config(scrollregion=(0, 0, total_width, 20))
    
    def update_gap_label(self, gap_index):
        """更新间隙时间标签"""
        # 获取间隙时间并格式化
        gap_time = self.gaps_ms[gap_index] / 1000.0  # 转换为秒
        gap_time_str = f"{gap_time:.1f}s"
        
        # 更新标签文本
        label_id = f"gap_label_{gap_index}"
        self.timeline_canvas.itemconfig(label_id, text=gap_time_str)
        
        # 居中放置标签
        gap_block = self.gap_blocks[gap_index]
        x1, y1, x2, y2 = self.timeline_canvas.coords(gap_block)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        
        # 获取标签的位置并更新
        self.timeline_canvas.coords(label_id, cx, cy)
    
    def add_gap_at_selection(self):
        """在选定的位置添加空白"""
        selected = self.files_listbox.curselection()
        if not selected:
            show_error("错误", "请先选择一个音频文件")
            return
        
        index = selected[0]
        duration_sec = self.gap_duration_var.get()
        duration_ms = int(duration_sec * 1000)
        
        # 如果是最后一个文件，添加到文件之后
        if index == len(self.audio_files) - 1:
            self.gaps_ms.append(duration_ms)
        else:
            # 否则插入到对应位置
            self.gaps_ms.insert(index, duration_ms)
        
        # 更新时间轴
        self.update_timeline()
    
    def update_timeline(self):
        """更新时间轴可视化"""
        # 清空画布
        self.timeline_canvas.delete("all")
        self.ruler_canvas.delete("all")
        self.audio_blocks = []
        self.gap_blocks = []
        
        if not self.audio_files:
            return
            
        # 起始x坐标
        x = 10
        
        # 绘制每个音频和间隙
        for i, (file_path, duration) in enumerate(zip(self.audio_files, self.audio_durations)):
            # 计算音频块宽度
            width = (duration / 1000.0) * self.timeline_scale  # 毫秒转秒，然后乘以比例
            
            # 绘制音频块
            audio_block = self.timeline_canvas.create_rectangle(
                x, 20, x + width, 100,
                fill="#90caf9", outline="#2196f3",
                tags=("audio", f"audio_{i}")
            )
            self.audio_blocks.append(audio_block)
            
            # 添加文件名标签
            filename = os.path.basename(file_path)
            if len(filename) > 20:
                filename = filename[:17] + "..."
            self.timeline_canvas.create_text(
                x + width/2, 60,
                text=filename,
                tags=f"audio_label_{i}"
            )
            
            # 添加时长标签
            duration_str = format_time(duration)
            self.timeline_canvas.create_text(
                x + width/2, 80,
                text=duration_str,
                tags=f"audio_duration_{i}"
            )
            
            # 如果有下一个音频，添加间隙
            if i < len(self.audio_files) - 1:
                # 确保有足够的间隙
                if i >= len(self.gaps_ms):
                    self.gaps_ms.append(0)
                
                # 计算间隙宽度
                gap_width = (self.gaps_ms[i] / 1000.0) * self.timeline_scale  # 毫秒转秒，然后乘以比例
                gap_width = max(10, gap_width)  # 确保最小宽度
                
                # 更新x坐标
                x += width
                
                # 绘制间隙块
                gap_block = self.timeline_canvas.create_rectangle(
                    x, 30, x + gap_width, 90,
                    fill="#e0e0e0", outline="#9e9e9e",
                    tags=("gap", f"gap_{i}")
                )
                self.gap_blocks.append(gap_block)
                
                # 添加间隙时间标签
                gap_time = self.gaps_ms[i] / 1000.0  # 转换为秒
                gap_label = self.timeline_canvas.create_text(
                    x + gap_width/2, 60,
                    text=f"{gap_time:.1f}s",
                    tags=f"gap_label_{i}"
                )
                
                # 更新x坐标
                x += gap_width
            else:
                # 更新x坐标到下一个位置
                x += width
        
        # 绘制时间标尺
        self.draw_time_ruler(x)
        
        # 设置画布滚动区域
        self.timeline_canvas.config(scrollregion=(0, 0, x + 50, 150))
        self.ruler_canvas.config(scrollregion=(0, 0, x + 50, 20))
    
    def draw_time_ruler(self, total_width):
        """绘制时间标尺"""
        # 计算总时长
        total_duration = sum(self.audio_durations) + sum(self.gaps_ms)
        total_seconds = math.ceil(total_duration / 1000.0)
        
        # 计算刻度间隔
        if self.timeline_scale <= 30:
            tick_interval = 10  # 每10秒一个刻度
        elif self.timeline_scale <= 60:
            tick_interval = 5   # 每5秒一个刻度
        elif self.timeline_scale <= 100:
            tick_interval = 2   # 每2秒一个刻度
        else:
            tick_interval = 1   # 每1秒一个刻度
        
        # 绘制刻度
        for sec in range(0, total_seconds + tick_interval, tick_interval):
            x = 10 + (sec * self.timeline_scale)
            if x > total_width:
                break
                
            # 绘制刻度线
            self.ruler_canvas.create_line(x, 0, x, 10, fill="#666")
            
            # 添加时间标签
            time_str = f"{sec}s"
            self.ruler_canvas.create_text(x, 15, text=time_str, anchor=tk.CENTER)
            
            # 在主画布上添加辅助线
            self.timeline_canvas.create_line(x, 0, x, 150, fill="#ddd", dash=(2, 4))
            
    def add_files(self):
        """
        添加音频文件到列表
        """
        files = load_multiple_audio_files()
        if files:
            for file in files:
                if file not in self.audio_files:
                    # 获取音频时长
                    try:
                        duration = get_audio_duration(file)
                        
                        self.audio_files.append(file)
                        self.audio_durations.append(duration)
                        self.files_listbox.insert(tk.END, os.path.basename(file))
                        
                        # 为每个添加的文件之间设置默认间隙为0
                        if len(self.audio_files) > 1 and len(self.gaps_ms) < len(self.audio_files) - 1:
                            self.gaps_ms.append(0)
                    except Exception as e:
                        show_error("错误", f"无法加载音频文件: {str(e)}")
            
            # 更新时间轴
            self.update_timeline()
    
    def update_gaps_ui(self):
        """
        更新间隙设置UI
        """
        # 清除现有的间隙设置UI
        for widget in self.gaps_frame.winfo_children():
            widget.destroy()
            
        # 如果没有文件或只有一个文件，则不需要设置间隙
        if len(self.audio_files) <= 1:
            ttk.Label(self.gaps_frame, text="需要至少两个音频文件\n才能设置间隙").pack(pady=20)
            return
            
        # 确保gaps_ms长度正确
        while len(self.gaps_ms) < len(self.audio_files) - 1:
            self.gaps_ms.append(0)
            
        # 为每两个文件之间创建一个间隙设置
        for i in range(len(self.audio_files) - 1):
            gap_frame = ttk.Frame(self.gaps_frame)
            gap_frame.pack(fill=tk.X, pady=2)
            
            file1 = os.path.basename(self.audio_files[i])
            file2 = os.path.basename(self.audio_files[i+1])
            
            ttk.Label(gap_frame, text=f"{file1} 和 {file2} 之间:").pack(side=tk.LEFT, padx=5)
            
            # 使用DoubleVar存储浮点数的秒数
            gap_var = tk.DoubleVar(value=self.gaps_ms[i]/1000.0)  # 转换为秒
            
            def create_callback(index, var):
                def callback(*args):
                    self.gaps_ms[index] = int(var.get() * 1000)  # 转换为毫秒
                return callback
                
            gap_var.trace_add("write", create_callback(i, gap_var))
            
            gap_spin = ttk.Spinbox(gap_frame, from_=0, to=60, increment=0.1, textvariable=gap_var, width=5)
            gap_spin.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(gap_frame, text="秒").pack(side=tk.LEFT)
    
    def clear_files(self):
        """
        清空文件列表
        """
        self.audio_files = []
        self.audio_durations = []
        self.gaps_ms = []
        self.files_listbox.delete(0, tk.END)
        
        # 清空时间轴
        self.update_timeline()
    
    def remove_selected(self):
        """
        移除选定的文件
        """
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            return
            
        # 从后往前删除，避免索引变化
        for i in sorted(selected_indices, reverse=True):
            del self.audio_files[i]
            del self.audio_durations[i]
            self.files_listbox.delete(i)
            
            # 更新间隙列表
            if i < len(self.gaps_ms):
                # 删除对应的间隙
                del self.gaps_ms[i]
            elif i > 0 and len(self.gaps_ms) > 0 and i == len(self.audio_files):
                # 如果删除最后一个文件，也要删除前一个间隙
                del self.gaps_ms[-1]
        
        # 更新时间轴
        self.update_timeline()
    
    def move_up(self):
        """
        上移选定文件
        """
        selected_indices = self.files_listbox.curselection()
        if not selected_indices or selected_indices[0] == 0:
            return
            
        idx = selected_indices[0]
        # 交换音频文件和时长
        self.audio_files[idx], self.audio_files[idx-1] = self.audio_files[idx-1], self.audio_files[idx]
        self.audio_durations[idx], self.audio_durations[idx-1] = self.audio_durations[idx-1], self.audio_durations[idx]
        
        # 更新文件之间的间隙
        if idx > 1 and idx - 2 < len(self.gaps_ms):
            # 如果移动的不是第二个文件，需要交换两个间隙
            self.gaps_ms[idx-2], self.gaps_ms[idx-1] = self.gaps_ms[idx-1], self.gaps_ms[idx-2]
        
        # 更新列表显示
        file_name = self.files_listbox.get(idx)
        self.files_listbox.delete(idx)
        self.files_listbox.insert(idx-1, file_name)
        self.files_listbox.selection_clear(0, tk.END)
        self.files_listbox.selection_set(idx-1)
        
        # 更新时间轴
        self.update_timeline()
    
    def move_down(self):
        """
        下移选定文件
        """
        selected_indices = self.files_listbox.curselection()
        if not selected_indices or selected_indices[0] == len(self.audio_files) - 1:
            return
            
        idx = selected_indices[0]
        # 交换音频文件和时长
        self.audio_files[idx], self.audio_files[idx+1] = self.audio_files[idx+1], self.audio_files[idx]
        self.audio_durations[idx], self.audio_durations[idx+1] = self.audio_durations[idx+1], self.audio_durations[idx]
        
        # 更新文件之间的间隙
        if idx < len(self.gaps_ms) and idx + 1 < len(self.gaps_ms):
            # 交换两个间隙
            self.gaps_ms[idx], self.gaps_ms[idx+1] = self.gaps_ms[idx+1], self.gaps_ms[idx]
        
        # 更新列表显示
        file_name = self.files_listbox.get(idx)
        self.files_listbox.delete(idx)
        self.files_listbox.insert(idx+1, file_name)
        self.files_listbox.selection_clear(0, tk.END)
        self.files_listbox.selection_set(idx+1)
        
        # 更新时间轴
        self.update_timeline()
    
    def preview_merge(self):
        """
        预览合并效果
        """
        if not self.audio_files:
            show_error("错误", "请先添加音频文件")
            return
            
        try:
            # 直接使用统一的预览接口
            AudioProcessor.preview_operation(
                self.audio_files,
                AudioProcessor.merge_audios_with_gaps,
                self.gaps_ms
            )
        except Exception as e:
            show_error("错误", f"预览音频失败: {str(e)}")
    
    def merge_files(self):
        """
        合并选定的音频文件
        """
        if not self.audio_files:
            show_error("错误", "请先添加音频文件")
            return
            
        try:
            output_path = save_audio_file()
            if not output_path:
                return
            
            # 使用带间隙的合并方法
            AudioProcessor.merge_audios_with_gaps(self.audio_files, output_path, self.gaps_ms)
            show_info("成功", f"已成功合并音频并保存到: {output_path}")
            
        except Exception as e:
            show_error("错误", f"合并音频失败: {str(e)}") 