import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt

class BoxApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('小算盒子')
        self.setFixedSize(1050, 580)

        self.listlabel = QLabel(self)
        self.listlabel.setGeometry(10, 10, 321, 281)
        self.listlabel.setStyleSheet("background-color: rgb(161, 155, 148)")
        self.listlabel.setText("设备列表")

        self.fileButton = QPushButton("文件管理", self)
        self.fileButton.setGeometry(360, 170, 70, 30)
        self.fileButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.addButton = QPushButton("添加设备", self)
        self.addButton.setGeometry(360, 90, 70, 30)
        self.addButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.deskButton = QPushButton("桌面显示", self)
        self.deskButton.setGeometry(360, 250, 70, 30)
        self.deskButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.scanButton = QPushButton("扫描设备", self)
        self.scanButton.setGeometry(360, 10, 70, 30)
        self.scanButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.executeButton = QPushButton("执行命令", self)
        self.executeButton.setGeometry(250, 370, 70, 30)
        self.executeButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.hookButton = QPushButton("一键HOOK", self)
        self.hookButton.setGeometry(10, 420, 70, 30)
        self.hookButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.menuButton = QPushButton("菜单键", self)
        self.menuButton.setGeometry(10, 320, 70, 30)
        self.menuButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.runButton = QPushButton("运行lamda", self)
        self.runButton.setGeometry(250, 320, 70, 30)
        self.runButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.homeButton = QPushButton("HOME键", self)
        self.homeButton.setGeometry(90, 320, 70, 30)
        self.homeButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.captureButton = QPushButton("一键抓包", self)
        self.captureButton.setGeometry(90, 420, 70, 30)
        self.captureButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.returnButton = QPushButton("返回键", self)
        self.returnButton.setGeometry(170, 320, 70, 30)
        self.returnButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.adbButton = QPushButton("输入框(ADB命令)", self)
        self.adbButton.setGeometry(10, 370, 230, 30)
        self.adbButton.setStyleSheet("background-color: rgb(152, 152, 152); border-radius: 5px;")

        self.hline = QFrame(self)
        self.hline.setFrameShape(QFrame.Shape.HLine)
        self.hline.setFrameShadow(QFrame.Shadow.Sunken)
        self.hline.setGeometry(0, 530, 1050, 21)

        self.idlabel = QLabel("设备ID:", self)
        self.idlabel.setGeometry(10, 550, 130, 15)

        self.equipmentlabel = QLabel("设备状态：", self)
        self.equipmentlabel.setGeometry(170, 550, 130, 15)

        self.vablabel = QLabel("VAB状态:", self)
        self.vablabel.setGeometry(340, 550, 130, 15)

        self.lamdalabel = QLabel("lamda状态:", self)
        self.lamdalabel.setGeometry(740, 550, 130, 15)

        self.rootlabel = QLabel("Root状态:", self)
        self.rootlabel.setGeometry(910, 550, 130, 15)

        self.namelabel = QLabel("设备名称：", self)
        self.namelabel.setGeometry(550, 550, 130, 15)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BoxApp()
    window.show()
    sys.exit(app.exec())
