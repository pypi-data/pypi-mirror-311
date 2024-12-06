import tkinter as tk
from tkinter import ttk

class SplitLayout(ttk.Frame):
    """左右布局组件"""
    
    def __init__(
        self,
        master,
        left_width: int = None,
        right_width: int = None,
        spacing: int = 10,
        separator: bool = True,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建一个容器来控制左右比例
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # 配置容器的列权重，确保左右均分
        self.container.grid_columnconfigure(0, weight=1, uniform='split')  # 使用 uniform 确保均分
        self.container.grid_columnconfigure(1, weight=0)  # 分隔线
        self.container.grid_columnconfigure(2, weight=1, uniform='split')  # 使用相同的 uniform 值
        self.container.grid_rowconfigure(0, weight=1)
        
        # 左侧面板
        self.left = ttk.Frame(self.container)
        if left_width:
            self.left.configure(width=left_width)
            self.left.grid_propagate(False)
        self.left.grid(row=0, column=0, sticky='nsew', padx=(0, spacing//2))
        
        # 分割线
        if separator:
            self.separator = ttk.Separator(self.container, orient='vertical')
            self.separator.grid(row=0, column=1, sticky='ns')
        
        # 右侧面板
        self.right = ttk.Frame(self.container)
        if right_width:
            self.right.configure(width=right_width)
            self.right.grid_propagate(False)
        self.right.grid(row=0, column=2, sticky='nsew', padx=(spacing//2, 0))
        
    def toggle_left(self):
        """切换左侧面板显示状态"""
        if self.left.winfo_ismapped():
            self.left.grid_remove()
            if hasattr(self, 'separator'):
                self.separator.grid_remove()
        else:
            self.left.grid(row=0, column=0, sticky='nsew')
            if hasattr(self, 'separator'):
                self.separator.grid(row=0, column=1, sticky='ns')
                
    def toggle_right(self):
        """切换右侧面板显示状态"""
        if self.right.winfo_ismapped():
            self.right.grid_remove()
            if hasattr(self, 'separator'):
                self.separator.grid_remove()
        else:
            if hasattr(self, 'separator'):
                self.separator.grid(row=0, column=1, sticky='ns')
            self.right.grid(row=0, column=2, sticky='nsew')