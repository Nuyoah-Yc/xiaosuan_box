import os
import tkinter as tk
from tkinter import filedialog

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QComboBox, QListWidget, QPushButton)
from lib.utils import show_devices,adb_shell

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.device_name_one = ""
        self.device_name_two = ""

        self.device_path_one = "/"
        self.device_reth_one = '/'

        self.device_path_two = "/"
        self.device_reth_two = '/'

        self.dst = '/data/local/tmp'
        # 主布局是水平布局
        self.layout = QHBoxLayout()

        # 左侧布局
        self.left_layout = QVBoxLayout()
        self.combo_box_left = QComboBox()
        self.list_widget_left = QListWidget()
        self.button_sest_rten_left = QPushButton("返回")
        self.button_to_delete_left = QPushButton("删除")
        self.button_add_file_left = QPushButton("上传(data/local/tmp)")
        self.button_dow_file_left = QPushButton("下载(项目目录的download)")
        self.left_layout.addWidget(self.combo_box_left)
        self.left_layout.addWidget(self.list_widget_left)
        self.left_layout.addWidget(self.button_sest_rten_left)
        self.left_layout.addWidget(self.button_to_delete_left)
        self.left_layout.addWidget(self.button_add_file_left)
        self.left_layout.addWidget(self.button_dow_file_left)
        self.combo_box_left.currentIndexChanged.connect(self.add_name_one)
        self.list_widget_left.itemDoubleClicked.connect(self.enter_directory_one)
        self.list_widget_left.itemClicked.connect(self.item_clicked_one)
        self.button_add_file_left.clicked.connect(self.update_file_one)
        self.button_sest_rten_left.clicked.connect(self.go_back_one)
        self.button_to_delete_left.clicked.connect(self.delete_file_one)
        self.button_dow_file_left.clicked.connect(self.download_file_one)


        # 中间按钮布局
        self.middle_layout = QVBoxLayout()
        self.button_to_cop = QPushButton("复制->")
        self.middle_layout.addStretch()
        self.middle_layout.addWidget(self.button_to_cop)
        self.middle_layout.addStretch()



        # 右侧布局
        self.right_layout = QVBoxLayout()
        self.combo_box_right = QComboBox()
        self.list_widget_right = QListWidget()
        self.button_sest_rten_right = QPushButton("返回")
        self.right_layout.addWidget(self.combo_box_right)
        self.right_layout.addWidget(self.list_widget_right)
        self.right_layout.addWidget(self.button_sest_rten_right)
        self.combo_box_right.currentIndexChanged.connect(self.add_name_two)
        self.list_widget_right.itemDoubleClicked.connect(self.enter_directory_two)
        self.button_sest_rten_right.clicked.connect(self.go_back_two)

        # 将布局添加到主布局中
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.middle_layout)
        self.layout.addLayout(self.right_layout)

        # 设置窗口的主布局
        self.setLayout(self.layout)

        # 初始化界面数据
        self.init_ui()

    def add_name_one(self):
        self.device_name_one = self.combo_box_left.currentText()
        self.update_device_files_one()
    def update_device_files_one(self):
        # 清空列表
        self.list_widget_left.clear()
        result = adb_shell.exec_command(f'adb -s {self.device_name_one} shell ls {self.device_path_one}',True)
        if result['out'] != 0:
            for file in result['out']:
                if file != "No output returned.":  # 确保不添加空字符串且过滤掉特定消息
                    self.list_widget_left.addItem(file)
                else:
                    self.go_back_one()
    def enter_directory_one(self, item):
        item_text = item.text()
        # 更新路径时，正确地添加斜杠
        new_path = os.path.join(self.device_path_one, item_text.replace("\r", ""))
        if not new_path.endswith('/'):
            new_path += '/'
        self.device_path_one = new_path
        try:
            self.update_device_files_one()
        except Exception as e:
            print("错误:", e)
    def go_back_one(self):
        path_parts = self.device_path_one.rstrip('/').split('/')
        if len(path_parts) > 1:
            self.device_path_one = '/'.join(path_parts[:-1]) + '/'
        else:
            self.device_path_one = '/'
        self.update_device_files_one()
    def item_clicked_one(self, item):
        item_text = item.text()
        new_path = os.path.join(self.device_path_one, item_text.replace("\r", ""))
        if new_path.endswith('/'):
            # 去掉最后面的斜杠
            new_path = new_path[:-1]

        self.device_reth_one = new_path
        print(self.device_reth_one)
    def delete_file_one(self):
        try:
            adb_shell.exec_command(f'adb -s {self.device_name_one} shell rm -rf "{self.device_reth_one}"',True)
            print(f"成功删除")
            self.update_device_files_one()
            self.update_device_files_two()
        except:
            print("删除失败:")
    def download_file_one(self):
        path = os.path.dirname(os.path.realpath(__file__))
        local_path = path.split("xiaosuan_box")[0] + "xiaosuan_box\download"
        try:
            adb_shell.exec_command(f'adb -s {self.device_name_one} pull "{self.device_reth_one}" "{local_path}"')
            return os.path.abspath(local_path) + "\\" + self.device_reth_one.split('/')[-1]
        except:
            print("下载失败:")





    def add_name_two(self):
        self.device_name_two = self.combo_box_right.currentText()
        self.update_device_files_two()
    def update_device_files_two(self):
        # 清空列表
        self.list_widget_right.clear()
        result = adb_shell.exec_command(f'adb -s {self.device_name_two} shell ls {self.device_path_two}',True)
        if result['out'] != 0:
            for file in result['out']:
                if file != "No output returned.":  # 确保不添加空字符串且过滤掉特定消息
                    self.list_widget_right.addItem(file)
                else:
                    self.go_back_two()
    def enter_directory_two(self, item):
        item_text = item.text()
        # 更新路径时，正确地添加斜杠
        new_path = os.path.join(self.device_path_two, item_text.replace("\r", ""))
        if not new_path.endswith('/'):
            new_path += '/'
        self.device_path_two = new_path
        try:
            self.update_device_files_two()
        except Exception as e:
            print("错误:", e)
    def go_back_two(self):
        path_parts = self.device_path_two.rstrip('/').split('/')
        if len(path_parts) > 1:
            self.device_path_two = '/'.join(path_parts[:-1]) + '/'
        else:
            self.device_path_two = '/'
        self.update_device_files_two()





    def init_ui(self):
        # 初始化下拉框和选择显示框的数据
        # 获取设备列表
        for i in show_devices.show_devices():
            self.combo_box_left.addItem(i)
            self.combo_box_right.addItem(i)

        # 复制按钮的点击事件
        self.button_to_cop.clicked.connect(self.copy_items)

    def copy_items(self):
        # 将左边选中的项复制到右边
        path_parts = self.download_file_one()
        adb_shell.adb_push(self.device_name_two, path_parts, self.device_path_two)
        self.update_device_files_two()

    def update_file_one(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title='选择一个文件上传到设备',
            filetypes=[('所有文件', '*.*')]  # 可以限定文件类型
        )
        if not file_path:
            return "没有选择文件"

        adb_shell.adb_push(self.device_name_one, file_path, self.dst)
        self.update_device_files_one()
        self.update_device_files_two()

def file_run():
    apps = QApplication([])
    windows = MainWindow()
    windows.show()
    apps.exec()

# file_run()