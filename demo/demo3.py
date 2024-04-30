import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
                             QWidget, QListWidget, QStatusBar, QSizePolicy)
from PyQt6.QtCore import Qt
from lib.utils import show_devices,adb_shell
# from lib.utils.file_management import file_run

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.device_name = ""


        # 设置窗口标题和大小
        self.setWindowTitle("小算科技逆向工具箱")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        # 主布局和中央窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()

        # 左侧布局：设备列表和按钮
        left_layout = QVBoxLayout()
        self.device_list = QListWidget()
        self.scan_button = QPushButton("扫描设备")
        self.add_button = QPushButton("添加设备")
        self.file_manager_button = QPushButton("文件管理")
        self.desktop_show = QPushButton("桌面显示")

        # 设置设备列表和按钮的尺寸策略
        policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.device_list.setSizePolicy(policy)
        self.scan_button.setSizePolicy(policy)
        self.add_button.setSizePolicy(policy)
        self.file_manager_button.setSizePolicy(policy)
        self.desktop_show.setSizePolicy(policy)

        left_layout.addWidget(self.device_list)
        left_layout.addWidget(self.scan_button)
        left_layout.addWidget(self.add_button)
        left_layout.addWidget(self.file_manager_button)
        left_layout.addWidget(self.desktop_show)
        self.device_list.itemClicked.connect(self.item_clicked)
        self.scan_button.clicked.connect(self.scan_button_op)
        # self.file_manager_button.clicked.connect(self.file_run)

        # 右侧布局：操作按钮
        right_layout = QVBoxLayout()
        self.hook_button = QPushButton("一键hook")
        self.capture_button = QPushButton("一键抓包")

        # 设置操作按钮的尺寸策略
        self.hook_button.setSizePolicy(policy)
        self.capture_button.setSizePolicy(policy)

        right_layout.addWidget(self.hook_button)
        right_layout.addWidget(self.capture_button)

        # 将左右布局加入主布局
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # 设置中央窗口的布局
        central_widget.setLayout(main_layout)

        # 状态栏显示设备信息
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        device_info = {
            '设备ID': '99061FFBA00648',
            '设备状态': '设备可能处于Recovery模式或已断开连接',
            'VAB状态': '槽位_A',
            '设备名称': 'coral',
            'Root状态': '未Root'
        }
        self.status_bar.showMessage(str(device_info))

    def scan_button_op(self):
        self.device_list.clear()
        for i in show_devices.show_devices():
            self.device_list.addItem(i)

    def item_clicked(self, item):
        item_text = item.text()
        self.device_name = item_text.replace("\r", "")
        print(self.device_name)




if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
