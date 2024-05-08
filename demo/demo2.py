import os
import sys
from tkinter import filedialog

from PIL._tkinter_finder import tk
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QFrame,
                             QListWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QDialog, QComboBox)
from lib.utils import adb_shell, show_devices
# from lib.tools import fridarpc
from lib.scrcpy import scrcpy

class FileSystem(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
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

class AddDeviceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('添加设备')
        self.setFixedSize(300, 100)

        layout = QVBoxLayout(self)

        self.deviceInput = QLineEdit(self)
        self.deviceInput.setPlaceholderText("输入IP地址，默认5555端口")
        layout.addWidget(self.deviceInput)

        self.addButton = QPushButton("添加", self)
        layout.addWidget(self.addButton)
        self.addButton.clicked.connect(self.add_device)

    def add_device(self):
        device_info = self.deviceInput.text()
        # 这里可以添加
        adb_shell.add_device(device_info)
        print(f"设备添加: {device_info}")  # 示例：打印信息
        self.accept()  # 关闭对话框


class BoxApp(QWidget):
    def __init__(self):
        super().__init__()
        self.fileSystemDialog = None
        self.devices = ''

        self.setWindowTitle('小算盒子')
        self.setFixedSize(1200, 600)

        # 创建主布局
        mainLayout = QHBoxLayout(self)

        # 创建左侧的列表框
        self.listlabel = QListWidget()
        self.listlabel.setFixedSize(300, 560)
        self.listlabel.itemClicked.connect(self.item_clicked)
        mainLayout.addWidget(self.listlabel)

        # 创建中间的按钮组
        buttonBox = QVBoxLayout()
        mainLayout.addLayout(buttonBox)

        # 第一组按钮
        deviceBox = QGroupBox("设备管理")
        deviceBoxLayout = QVBoxLayout()
        deviceBox.setLayout(deviceBoxLayout)
        self.scanButton = QPushButton("扫描设备")
        self.addButton = QPushButton("添加设备")
        self.fileButton = QPushButton("文件管理")
        self.deskButton = QPushButton("桌面显示")
        self.runButton = QPushButton("运行lamda")
        for button in [self.scanButton, self.addButton, self.fileButton, self.deskButton, self.runButton]:
            deviceBoxLayout.addWidget(button)
        buttonBox.addWidget(deviceBox)
        self.scanButton.clicked.connect(self.scan)
        self.addButton.clicked.connect(self.show_add_device_dialog)
        self.fileButton.clicked.connect(self.show_file_system)
        self.deskButton.clicked.connect(self.deskButtons)

        # 第二组按钮
        controlBox = QGroupBox("控制键")
        controlBoxLayout = QVBoxLayout()
        controlBox.setLayout(controlBoxLayout)
        self.menuButton = QPushButton("菜单键")
        self.homeButton = QPushButton("HOME键")
        self.returnButton = QPushButton("返回键")
        for button in [self.returnButton, self.homeButton, self.menuButton]:
            controlBoxLayout.addWidget(button)
        buttonBox.addWidget(controlBox)
        self.menuButton.clicked.connect(self.menuButtons)
        self.homeButton.clicked.connect(self.homeButtons)
        self.returnButton.clicked.connect(self.returnButtons)



        # 第三组按钮
        commandBox = QGroupBox("命令执行")
        commandBoxLayout = QVBoxLayout()
        commandBox.setLayout(commandBoxLayout)
        self.adbLineEdit = QLineEdit()
        self.executeButton = QPushButton("执行命令，不用加adb shell ")
        self.hookButton = QPushButton("一键HOOK")
        self.captureButton = QPushButton("一键抓包")
        commandBoxLayout.addWidget(self.adbLineEdit)
        for button in [self.executeButton, self.hookButton, self.captureButton]:
            commandBoxLayout.addWidget(button)
        buttonBox.addWidget(commandBox)

        # 状态标签组
        statusBox = QGroupBox("设备状态")
        statusBoxLayout = QHBoxLayout()
        statusBox.setLayout(statusBoxLayout)
        self.idlabel = QLabel("设备ID:")
        self.equipmentlabel = QLabel("设备状态：")
        self.vablabel = QLabel("VAB状态:")
        self.lamdalabel = QLabel("lamda状态:")
        self.rootlabel = QLabel("Root状态:")
        self.namelabel = QLabel("设备名称：")
        for label in [self.idlabel, self.equipmentlabel, self.vablabel, self.lamdalabel, self.rootlabel,
                      self.namelabel]:
            statusBoxLayout.addWidget(label)
        buttonBox.addWidget(statusBox)

        self.setLayout(mainLayout)


    def scan(self):
        self.listlabel.clear()
        devices_list = show_devices.show_devices()
        for device in devices_list:
            self.listlabel.addItem(device)

    def item_clicked(self,item):
        item_text = item.text().replace("\r", "")
        self.devices = item_text
        print(self.devices)

    def show_add_device_dialog(self):
        dialog = AddDeviceDialog(self)
        dialog.exec()  # 显示对话框并等待关闭
        self.scan()

    def show_file_system(self):
        if self.fileSystemDialog is None:  # 创建对话框实例，如果它还不存在
            self.fileSystemDialog = FileSystem(self)
        self.fileSystemDialog.show()
        # pass

    def menuButtons(self):
        show_devices.button_recent(self.devices)

    def homeButtons(self):
        show_devices.button_home(self.devices)

    def returnButtons(self):

        show_devices.button_back(self.devices)

    def deskButtons(self):
        scrcpy.start_scrcpy(self.devices)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BoxApp()
    window.show()
    sys.exit(app.exec())
