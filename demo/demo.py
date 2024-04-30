from lib.utils import adb_shell, file_updata, show_devices
import tkinter as tk, os
from tkinter import filedialog

from lib.scrcpy import scrcpy















if __name__ == '__main__':
    devices = show_devices.show_devices()
    print(devices)
    # print(show_devices.get_device_info(devices[0]))
    # print(file_updata.update_file(devices[0]))
    # scrcpy.start_scrcpy(devices[1])
    file_updata.run_file_downloader('192.168.121.231:65000')
    # print(adb_shell.add_device('192.168.121.231:65000'))