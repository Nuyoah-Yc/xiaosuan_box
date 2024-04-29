import tkinter as tk
import subprocess

import tkinter as tk, os
from tkinter import filedialog
from lib.utils import adb_shell


class FileDownloader(tk.Tk):
    def __init__(self, device_name):
        super().__init__()
        self.device_name = device_name
        self.title("Android File Downloader")
        self.geometry("600x450")  # 窗口尺寸
        self.device_path = "/"
        self.create_widgets()
        self.update_file_list()

    def create_widgets(self):
        self.lbl = tk.Label(self, text="选择文件下载:")
        self.lbl.grid(row=0, column=0, padx=10, pady=10)

        self.lst_files = tk.Listbox(self, width=50, height=15)
        self.lst_files.grid(row=1, column=0, padx=20, pady=10)
        self.lst_files.bind('<Double-1>', self.enter_directory)  # 双击进入目录

        self.btn_back = tk.Button(self, text="返回", command=self.go_back)
        self.btn_back.grid(row=2, column=0, padx=10, pady=10)

        self.btn_download = tk.Button(self, text="下载", command=self.download_file)
        self.btn_download.grid(row=3, column=0, padx=10, pady=10)

    def update_file_list(self):
        self.lst_files.delete(0, tk.END)
        command = ["adb", "-s", self.device_name, "shell", "ls", "-1", self.device_path]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            files = result.stdout.split('\n')
            for file in files:
                if file:  # 确保不添加空字符串
                    self.lst_files.insert(tk.END, file)
        else:
            print("错误:", result.stderr)
            if "Not a directory" in result.stderr:
                self.handle_not_a_directory()

    def handle_not_a_directory(self):
        # 尝试返回上一级目录
        if self.device_path != '/':
            path_parts = self.device_path.rstrip('/').split('/')
            if len(path_parts) > 1:
                self.device_path = '/'.join(path_parts[:-1]) + '/'
            else:
                self.device_path = '/'
            self.update_file_list()
        else:
            print("已在根目录，无法返回。")

    def enter_directory(self, event):
        selected_index = self.lst_files.curselection()
        if selected_index:
            selected_item = self.lst_files.get(selected_index[0]).strip('/')
            # 构建可能的新路径
            new_path = os.path.join(self.device_path, selected_item)
            if not new_path.endswith('/'):
                new_path += '/'
            # 尝试更新目录列表
            try:
                self.device_path = new_path
                self.update_file_list()
            except Exception as e:
                print("错误:", e)
                print(f"无法进入 {selected_item}，可能是一个文件或没有权限访问。")

    def go_back(self):
        if self.device_path != '/':
            # 移除尾部的斜杠（如果存在），然后分割路径
            path_parts = self.device_path.rstrip('/').split('/')
            # 如果路径可以返回上一级（长度大于1），则重新组合路径，否则保持根目录
            if len(path_parts) > 1:
                self.device_path = '/'.join(path_parts[:-1]) + '/'
            else:
                self.device_path = '/'
            self.update_file_list()

    def download_file(self):
        selected_index = self.lst_files.curselection()
        if selected_index:
            selected_file = self.lst_files.get(selected_index[0])
            local_path = "../download/"
            adb_command = f'adb -s "{self.device_name}" pull "{self.device_path}{selected_file}" "{local_path}"'
            try:
                subprocess.run(adb_command, shell=True, check=True)
                print(f"文件已下载到: {os.path.abspath(local_path)}")
            except subprocess.CalledProcessError as e:
                print("下载失败:", e)
        else:
            print("没有选择文件")

def update_file(serial,dst='/data/local/tmp'):
    """
    打开资源管理器选择文件并上传到 Android 设备的 /data/local/tmp 目录。(默认/data/local/tmp)
    参数:
    serial (str): 设备的序列号。
    """
    # 创建一个 Tkinter 根窗口并隐藏
    root = tk.Tk()
    root.withdraw()

    # 打开文件选择对话框
    file_path = filedialog.askopenfilename(
        title='选择一个文件上传到设备',
        filetypes=[('所有文件', '*.*')]  # 可以限定文件类型
    )

    # 用户取消选择
    if not file_path:
        return "没有选择文件"

    # 获取文件名作为目标文件名
    # file_name = os.path.basename(file_path)

    # 调用 adb_push 方法上传文件
    result = adb_shell.adb_push(serial, file_path, dst)
    return f'上传结果: {result["out"][0]}'

def run_file_downloader(device_name):
    app = FileDownloader(device_name)
    app.mainloop()

