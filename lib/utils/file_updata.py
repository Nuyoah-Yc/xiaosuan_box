
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
        self.lbl = tk.Label(self, text="选择文件或目录进行操作:")
        self.lbl.grid(row=0, column=0, padx=10, pady=10)

        self.lst_files = tk.Listbox(self, width=50, height=15)
        self.lst_files.grid(row=1, column=0, padx=20, pady=10)
        self.lst_files.bind('<Double-1>', self.enter_directory)  # 双击进入目录

        self.btn_back = tk.Button(self, text="返回", command=self.go_back)
        self.btn_back.grid(row=2, column=0, padx=10, pady=10)

        self.btn_download = tk.Button(self, text="下载", command=self.download_file)
        self.btn_download.grid(row=3, column=0, padx=10, pady=10)

        self.btn_delete = tk.Button(self, text="删除", command=self.delete_file)
        self.btn_delete.grid(row=4, column=0, padx=10, pady=10)

    def update_file_list(self):
        self.lst_files.delete(0, tk.END)
        command = ["adb", "-s", self.device_name, "shell", "ls", "-1", self.device_path]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            files = result.stdout.split('\n')
            for file in files:
                if file:  # 确保不添加空字符串
                    # print(file)
                    self.lst_files.insert(tk.END, file)
        else:
            print("错误:", result.stderr)

    def enter_directory(self, event):
        selected_index = self.lst_files.curselection()
        print(selected_index)
        if selected_index:
            selected_item = self.lst_files.get(selected_index[0]).strip('/')
            new_path = os.path.join(self.device_path, selected_item)
            if not new_path.endswith('/'):
                new_path += '/'
            try:
                self.device_path = new_path
                self.update_file_list()
            except Exception as e:
                print("错误:", e)

    def go_back(self):
        path_parts = self.device_path.rstrip('/').split('/')
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

    def delete_file(self):
        selected_index = self.lst_files.curselection()
        if selected_index:
            selected_file = self.lst_files.get(selected_index[0])
            adb_command = f'adb -s "{self.device_name}" shell rm -rf "{self.device_path}{selected_file}"'
            try:
                result = subprocess.run(adb_command, shell=True, check=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"成功删除: {selected_file}")
                    self.update_file_list()
                else:
                    print("删除失败:", result.stderr)
            except subprocess.CalledProcessError as e:
                print("删除失败:", e)
        else:
            print("没有选择文件或目录")



def run_file_downloader(device_name):
    app = FileDownloader(device_name)
    app.mainloop()

