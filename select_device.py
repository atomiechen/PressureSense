import argparse
import pyqtgraph as pg
import array
import serial
from serial.tools.list_ports import comports
import threading
import numpy as np
from queue import Queue
import time
from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtGui
import pytz
from datetime import datetime, timedelta

BAUDRATE = 1000000
devices_found = comports()
PORT = None
try:
    ## default use the last port on the list
    PORT = devices_found[-1].device
except:
    pass


data_bytes = bytearray()
mSerial = None


def enumerate_ports():
    # 查看可用端口
    print("All serial ports:")
    for item in devices_found:
        print(item)

def serial_xx(gui, mSerial):
    global data_bytes
    print(f"mSerial: {mSerial}")
    while True:
        count = mSerial.inWaiting()
        if count:
            rec_str = mSerial.read(count)
            data_bytes = data_bytes + rec_str
            data_len = len(data_bytes)
            k = 0
            while k + 14 <= data_len:
                # 收到主机目前正在搜索的蓝牙名称
                if data_bytes[k] == 0XEE and data_bytes[k + 1] == 0X88 and data_bytes[k + 12] == 0XEE and data_bytes[k + 13] == 0X77:
                    name_buffer = ""
                    for k5 in range(10):
                        if data_bytes[k + 2 + k5] != 0xEE:
                            name_buffer = name_buffer + chr(data_bytes[k + 2 + k5])
                    gui.acupoint_name_select.setText("搜索目标：" + name_buffer)
                    k = k + 14
                else:
                    k = k + 1
            data_bytes[0:k] = b''


class MainWidget(QtWidgets.QMainWindow):

    # @staticmethod
    def action_refresh(self):
        self.mSerial.write(("RR").encode())

    def action_update(self):
        data_send_update = self.acupoint_name_select.text()
        print("data_send_update值为：" + data_send_update)
        self.mSerial.write((data_send_update + "UU").encode())

    def __init__(self, mSerial):
        self.mSerial = mSerial
        super().__init__()
        self.setWindowTitle("Select Device")  # 设置窗口标题
        self.main_widget = QtWidgets.QWidget()  # 实例化一个widget部件
        self.main_layout = QtWidgets.QGridLayout()  # 实例化一个网格布局层
        self.main_widget.setLayout(self.main_layout)  # 设置主widget部件的布局为网格布局
        # main_widget.setStyleSheet('QWidget{background:white;}')  # 设置背景为白色
        self.main_widget.setFixedSize(400, 600)

        # 增添选择设备编号的文本框和按钮
        self.acupoint_name_select = QtWidgets.QLineEdit()
        self.acupoint_name_select.setAlignment(Qt.AlignCenter)
        self.acupoint_name_select.setText('请选择设备编号')
        self.main_layout.addWidget(self.acupoint_name_select, 1, 1, alignment=Qt.AlignCenter)

        # 刷新按钮
        self.refreshButton = QtWidgets.QPushButton(self.main_widget)
        self.refreshButton.setText("Refresh")

        self.refreshButton.clicked.connect(self.action_refresh)
        self.main_layout.addWidget(self.refreshButton, 2, 1, alignment=Qt.AlignCenter)

        # 更新按钮
        self.updateButton = QtWidgets.QPushButton(self.main_widget)
        self.updateButton.setText("Update")

        self.updateButton.clicked.connect(self.action_update)
        self.main_layout.addWidget(self.updateButton, 3, 1, alignment=Qt.AlignCenter)

        self.setCentralWidget(self.main_widget)  # 设置窗口默认部件为主widget


def main(args):
    if args.enumerate:
        enumerate_ports()
        return

    app = QtWidgets.QApplication(sys.argv)
    mSerial = serial.Serial(args.port, args.baudrate, timeout=0.1)
    if mSerial.isOpen():
        print("open success")
        mSerial.flushInput()  # 清空缓冲区

    else:
        print("open failed")
        mSerial.close()  # 关闭端口
    gui = MainWidget(mSerial)
    th1 = threading.Thread(target=serial_xx, args=(gui,mSerial))
    th1.start()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-e', dest='enumerate', action=('store_true'), default=False, help="enumerate all serial ports")
    parser.add_argument('-p', dest='port', action=('store'), default=PORT, help="specify serial port")
    parser.add_argument('-b', dest='baudrate', action=('store'), default=BAUDRATE, type=int, help="specify baudrate")
    args = parser.parse_args()

    main(args)
