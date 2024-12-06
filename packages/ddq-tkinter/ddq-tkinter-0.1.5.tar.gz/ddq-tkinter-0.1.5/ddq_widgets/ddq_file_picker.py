import tkinter as tk
from tkinter import ttk
from tkinter import filedialog  # 添加这行
from typing import Optional, List, Tuple, Literal

class FilePicker(ttk.Frame):
    def __init__(
        self,
        master,
        label: str = "",
        mode: str = "file",  # file/folder
        filetypes: List[Tuple[str, str]] = None,
        multiple_buttons: bool = False,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 创建路径变量
        self.path_var = tk.StringVar()
        
        # 创建输入框
        self.entry = ttk.Entry(self, textvariable=self.path_var)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        if multiple_buttons:
            # 创建文件选择按钮
            self.file_button = ttk.Button(
                self,
                text="选择文件",
                command=self._select_file
            )
            self.file_button.pack(side=tk.LEFT, padx=(2, 0))
            
            # 创建文件夹选择按钮
            self.folder_button = ttk.Button(
                self,
                text="选择目录",
                command=self._select_folder
            )
            self.folder_button.pack(side=tk.LEFT, padx=(2, 0))
        else:
            # 创建单个选择按钮
            button_text = "选择目录" if mode == "folder" else "选择文件"
            command = self._select_folder if mode == "folder" else self._select_file
            self.button = ttk.Button(
                self,
                text=button_text,
                command=command
            )
            self.button.pack(side=tk.LEFT, padx=(2, 0))
            
        self.mode = mode
        self.filetypes = filetypes or [("All files", "*.*")]
        
        # 添加 value 属性的 getter 和 setter
        self._value = ""
        
    def _select_file(self):
        """选择文件"""
        path = filedialog.askopenfilename(filetypes=self.filetypes)
        if path:
            self.path_var.set(path)
            
    def _select_folder(self):
        """选择文件夹"""
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
            
    @property
    def value(self) -> str:
        """获取当前选择的路径"""
        return self.path_var.get()
        
    @value.setter
    def value(self, path: str):
        """设置路径值"""
        self.path_var.set(path or "")  # 确保空值处理
        if hasattr(self, 'entry'):
            self.entry.delete(0, tk.END)
            self.entry.insert(0, path or "")
        
    def set_state(self, state: str):
        """设置组件状态"""
        self.entry.configure(state=state)
        if hasattr(self, 'button'):
            self.button.configure(state=state)
        if hasattr(self, 'file_button'):
            self.file_button.configure(state=state)
            self.folder_button.configure(state=state)