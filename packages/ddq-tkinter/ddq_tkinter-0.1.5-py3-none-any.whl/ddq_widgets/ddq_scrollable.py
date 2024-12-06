import tkinter as tk
from tkinter import ttk

class ScrollableContainer(ttk.Frame):
    """通用的可滚动容器组件
    
    特性：
    1. 支持任意内容的垂直滚动
    2. 自动/始终/从不显示滚动条
    3. 支持鼠标滚轮
    4. 自动适应内容高度
    """
    
    def __init__(
        self,
        master,
        scrollbar: str = "auto",  # auto/always/never
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 确保容器本身填充父组件
        self.pack(fill=tk.BOTH, expand=True)
        
        # 使用 Canvas 作为滚动容器
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content = ttk.Frame(self.canvas)
        
        # 配置 Canvas
        self.canvas.configure(yscrollcommand=self._on_scroll)
        self.canvas_window = self.canvas.create_window(
            (0, 0), 
            window=self.content,
            anchor="nw",
            width=self.canvas.winfo_width()  # 设置内容宽度
        )
        
        # 布局
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        if scrollbar != "never":
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        # 绑定事件
        self.content.bind("<Configure>", self._on_content_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)
        
        self._scrollbar_mode = scrollbar
        
    def _on_scroll(self, *args):
        """滚动条位置改变时的回调"""
        self.scrollbar.set(*args)
        # 根据内容处理滚动条显示
        if self._scrollbar_mode == "auto":
            if self.content.winfo_reqheight() > self.canvas.winfo_height():
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                self.scrollbar.pack_forget()
                
    def _on_content_configure(self, event):
        """内容大小改变时更新滚动区域"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_canvas_configure(self, event):
        """Canvas大小改变时调整内容宽度"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        
    def _bind_mousewheel(self, event):
        """鼠标进入时绑定滚轮事件"""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _unbind_mousewheel(self, event):
        """鼠标离开时解绑滚轮事件"""
        self.canvas.unbind_all("<MouseWheel>")
        
    def _on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        if self.scrollbar.winfo_ismapped():  # 只在显示滚动条时响应
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units") 